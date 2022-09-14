import torch
import prefect
from prefect import task, Flow, Parameter
from prefect.triggers import all_successful, any_successful
from prefect.engine import signals
import matplotlib.pyplot as plt
import numpy as np
import client_data
import json

class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.in_features = input_dim
        self.out_features = output_dim
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):
        outputs = torch.sigmoid(self.linear(x))
        return outputs

def client_set_ml_model(client, model_dict):
    return client.call("set_ml_model", model_dict)

def client_set_loss_fn(client, loss_fn):
    return client.call("set_loss_fn", loss_fn)

def client_set_opt_method(client, opt_method, model, learning_rate):
    return client.call("set_opt_method", (opt_method, model, learning_rate))

def client_get_grads(client, model, loss_fn, inputs, outputs):
    return client.call("get_grads", (model, loss_fn, inputs, outputs))

def client_update_grads(client, model, opt, gradients):
    return client.call("update_grads", (model, opt, gradients))

def client_agg_grads(client, party_grads):
    return client.call("agg_gradients", party_grads)

def client_predict(client, model, inputs, threshold):
    return client.call("predict", (model, inputs, threshold))

def client_calc_conf_mat(client, y_true, y_preds):
    return client.call("calc_conf_mat", (y_true, y_preds))

class FederatedLogisticRegression:
    def __init__(self, clients):
        self.clients = clients
        self.loss_fn = []
        self.opt = []
        self.models = []
        self.in_features = 0
        self.out_features = 0
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
    
    def model_setup(self, lr = 1e-5, loss_fn = "BCELoss", opt_method = "SGD"):
        shapeX = client_data.client_df_get_shape(self.clients[0], self.x_train[0])
        self.in_features = shapeX[1]
        self.out_features = 1
        global_model = LogisticRegression(self.in_features, self.out_features)
        global_model_dict = {"in":shapeX[1], "out":1, "state":global_model.state_dict()}
        for key in global_model_dict["state"]:
            if isinstance(global_model_dict["state"][key], torch.Tensor):
                global_model_dict["state"][key] = {"value":global_model_dict["state"][key].tolist(), "changed":True}
        for i in range(len(self.clients)):
            model = client_set_ml_model(self.clients[i], global_model_dict)
            self.models.append(model)
            self.loss_fn.append(client_set_loss_fn(self.clients[i], loss_fn))
            self.opt.append(client_set_opt_method(self.clients[i], opt_method, model, lr))        
    
    def data_setup(self, X, y, train_test_ratio):
        for i in range(len(self.clients)):
            xtr, xte, ytr, yte = client_data.client_train_test_split(self.clients[i], X[i], y[i], train_test_ratio)
            xtr = client_data.client_df_to_torch_tensor(self.clients[i], xtr)
            xte = client_data.client_df_to_torch_tensor(self.clients[i], xte)
            ytr = client_data.client_df_to_torch_tensor(self.clients[i], ytr)
            yte = client_data.client_df_to_torch_tensor(self.clients[i], yte)
            self.x_train.append(xtr)
            self.x_test.append(xte)
            self.y_train.append(ytr)
            self.y_test.append(yte)
    
    def _collect_grads(self):
        grads_list = []
        for i in range(len(self.clients)):
            grads = client_get_grads(self.clients[i], self.models[i], self.loss_fn[i], self.x_train[i], self.y_train[i])
            grads_list.append(grads)
        return {"value": grads_list, "compressed": False}
    
    def _update_grads(self, gradients):
        models = []
        opts = []
        for i in range(len(self.clients)):
            res = client_update_grads(self.clients[i], self.models[i], self.opt[i], gradients)
            models.append(res)
        #    opts.append(res[1])
        self.models=models
        #self.opt = opts
    
    def _agg_grads(self, party_grads):
        new_grads = client_agg_grads(self.clients[0], party_grads)
        return new_grads
    
    def fit(self, epochs):
        for epoch in range(epochs):
            grads_list = self._collect_grads()
            new_grads  = self._agg_grads(grads_list)
            self._update_grads(new_grads)
    
    def predict(self, model, inputs, threshold = 0.5):
        results = []
        for client in range(len(self.clients)):
            res = client_predict(client, model, inputs, threshold)
            results.append(res)
        return results
    
    def report(self):
        tprs = []
        fprs = []
        thrs = []
        for k in range(101):
            conf_mat_all = 0
            thr = float(k)/100
            for i in range(len(self.clients)):
                pred = client_predict(self.clients[i], self.models[i], self.x_test[i], threshold = thr)
                conf_mat = client_calc_conf_mat(self.clients[i], self.y_test[i], pred)
                conf_mat = np.array(conf_mat)
                conf_mat_all += conf_mat
            true_positive = conf_mat_all[0, 0]
            false_negative = conf_mat_all[1, 0]
            false_positive = conf_mat_all[0, 1]
            true_negative = conf_mat_all[1, 1]
            tprs.append(float(true_positive) / (true_positive + false_negative))
            fprs.append(float(false_positive) / (false_positive + true_negative))
            thrs.append(thr)
        print(fprs)
        print(tprs)
        plt.plot(fprs, tprs)
        plt.show()
    
    def run_graph(self, X, y, train_test_ratio = 0.2, loss_fn = "BCELoss", opt_method = "SGD", epoch = 100, learn_rate = 0.05):
        
        task_set_model = task(client_set_ml_model)
        task_set_loss_fn = task(client_set_loss_fn)
        task_set_opt_method = task(client_set_opt_method)
        #task_get_grads = task(client_get_grads)
        #task_update_grads = task(client_update_grads)
        #task_agg_grads = task(client_agg_grads)
        task_train_test_split = task(client_data.client_train_test_split)
        task_df_to_torch_tensor = task(client_data.client_df_to_torch_tensor)
        #task_predict = task(client_predict)
        #task_conf_mat = task(client_calc_conf_mat)
        task_df_get_shape = task(client_data.client_df_get_shape)
        
        @task
        def create_model(shapeX):
            in_features = shapeX[1]
            out_features = 1
            global_model = LogisticRegression(in_features, out_features)
            global_model_dict = {"in":shapeX[1], "out":1, "state":global_model.state_dict()}
            for key in global_model_dict["state"]:
                if isinstance(global_model_dict["state"][key], torch.Tensor):
                    global_model_dict["state"][key] = {"value":global_model_dict["state"][key].tolist(), "changed":True}
            return global_model_dict
        
        @task
        def train(clients, models, loss_fns, opt_methods, X_trains, y_trains):
            print("training")
            for k in range(100):
                grads_list = []
                for i in range(len(clients)):
                    grads = client_get_grads(clients[i], models[i], loss_fns[i], X_trains[i], y_trains[i])
                    grads_list.append(grads)

                new_grads = client_agg_grads(clients[0], {"value": grads_list, "compressed": False})

                for i in range(len(clients)):
                    res = client_update_grads(clients[i], models[i], opt_methods[i], new_grads)
                    models[i] = res

            return models
        
        @task
        def test(clients, models, X_tests, y_tests):
            print("test")
            tprs = []
            fprs = []
            thrs = []
            for k in range(101):
                conf_mat_all = 0
                thr = float(k)/100
                for i in range(len(clients)):
                    pred = client_predict(clients[i], models[i], X_tests[i], threshold = thr)
                    conf_mat = client_calc_conf_mat(clients[i], y_tests[i], pred)
                    conf_mat = np.array(conf_mat)
                    conf_mat_all += conf_mat
                true_positive = conf_mat_all[0, 0]
                false_negative = conf_mat_all[1, 0]
                false_positive = conf_mat_all[0, 1]
                true_negative = conf_mat_all[1, 1]
                tprs.append(float(true_positive) / (true_positive + false_negative))
                fprs.append(float(false_positive) / (false_positive + true_negative))
                thrs.append(thr)
            return (tprs, fprs)
        
        with Flow("fed_logistic_regression") as f:
            parameter_X = Parameter("X", default = X)
            parameter_y = Parameter("y", default = y)
            parameter_train_test_ratio = Parameter("train_test_ratio", default = train_test_ratio)
            parameter_loss_fn = Parameter("loss_fn", default = loss_fn)
            parameter_opt_method = Parameter("opt", default = opt_method)
            #parameter_epoch = Parameter("epoch", default = epoch)
            parameter_lr = Parameter("lr", default = learn_rate)
            
            models = []
            loss_fns = []
            opt_methods = []
            X_trains = []
            X_tests = []
            y_trains = []
            y_tests = []
            
            shapeX = 0
            for i in range(len(self.clients)):
                res= task_train_test_split(self.clients[i], parameter_X[i], parameter_y[i], parameter_train_test_ratio)
                shapeX = task_df_get_shape(self.clients[i], res[0])
                xtr = task_df_to_torch_tensor(self.clients[i], res[0])
                xte = task_df_to_torch_tensor(self.clients[i], res[1])
                ytr = task_df_to_torch_tensor(self.clients[i], res[2])
                yte = task_df_to_torch_tensor(self.clients[i], res[3])
                X_trains.append(xtr)
                X_tests.append(xte)
                y_trains.append(ytr)
                y_tests.append(yte)

            global_model_dict = create_model(shapeX)
            
            for i in range(len(self.clients)):
                model = task_set_model(self.clients[i], global_model_dict)
                models.append(model)
                loss_fns.append(task_set_loss_fn(self.clients[i], parameter_loss_fn))
                opt_methods.append(task_set_opt_method(self.clients[i], parameter_opt_method, model, parameter_lr))
            
            models = train(self.clients, models, loss_fns, opt_methods, X_trains, y_trains)
            res = test(self.clients, models, X_tests, y_tests)
        
        state = f.run()
        ploty = state.result[res].result[0]
        plotX = state.result[res].result[1]
        plt.plot(plotX, ploty)
        plt.show()
        
        return state

            
            