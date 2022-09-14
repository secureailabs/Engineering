import torch
import copy
from sklearn.metrics import recall_score, precision_score, accuracy_score, confusion_matrix
from typing import List, Type, List, Tuple
from zero import SecretObject, TorchLinearModel
import numpy as np

class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.in_features = input_dim
        self.out_features = output_dim
        self.linear = torch.nn.Linear(input_dim, output_dim)
        
    def forward(self, x):
        outputs = torch.sigmoid(self.linear(x))
        return outputs

def set_loss_fn(fn_label:str) -> Type[SecretObject]:
    fn = 0
    if(fn_label == "BCELoss"):
        fn = torch.nn.BCELoss()
    return SecretObject(fn)

def set_opt_method(opt_label:str, model: Type[SecretObject], learn_rate:float) -> Type[SecretObject]:
    opt = 0
    if(opt_label == "SGD"):
        opt = torch.optim.SGD(model.parameters(), lr=learn_rate)
    return SecretObject(opt)

def set_ml_model(model_dict: dict) -> Type[SecretObject]:
    model = LogisticRegression(model_dict["in"], model_dict["out"])
    for key in model_dict["state"]:
        if "changed" in model_dict["state"][key]:
            model_dict["state"][key] = torch.Tensor(model_dict["state"][key]["value"])
    model.load_state_dict(model_dict["state"])
    print(model.state_dict())
    return SecretObject(model)

def get_grads(model: Type[SecretObject], loss_fn: Type[SecretObject], inputs: Type[SecretObject], outputs: Type[SecretObject]) -> list:
    pred = model(inputs)
    loss = loss_fn(pred, outputs)
    loss.backward()
    gradients = []
    for p in model.parameters():
        #print(p.grad)
        gradients.append(p.grad.tolist())
    return gradients

def update_grads(model: Type[SecretObject], opt: Type[SecretObject], gradients: List) -> Type[SecretObject]:
    for i, p in enumerate(model.parameters()):
        grad = torch.Tensor(gradients[i])
        print("-------before--------")
        print(p)
        print(grad)
        p.data = p - 0.5 * grad
        print("-------after--------")
        print(p)
#     for i, p in enumerate(model.parameters()):
#         p.grad = copy.deepcopy(torch.Tensor(gradients[i]))
#         print(p.grad)
#     print("=============grads============")
#     for p in opt.param_groups[0]['params']:
#         if p.grad is None:
#             print("p is none")
#         else:
#             print(p.grad)
#     print("----------before----------")
#     print(model.state_dict())
#     opt.step()
#     opt.zero_grad()
#     print("----------after----------")
#     print(model.state_dict())
#     print(opti.param_groups)
    return SecretObject(model)

def agg_gradients(party_grads: List)-> List:
    parties = len(party_grads)
    new_gradients = []
    for i in range(len(party_grads[0])):
        tot = 0
        for j in range(parties):
            tot += np.array(party_grads[j][i]) 
        res = tot/parties
        new_gradients.append(res.tolist())
    return new_gradients

def predict(model: Type[SecretObject], inputs: Type[SecretObject], threshold: float) -> Type[SecretObject]:
    preds = model(inputs)
    preds = preds.cpu().detach().numpy()
    #print(preds.T)
    preds = (preds > threshold).astype(int)
    #print(preds.T.tolist())
    return SecretObject(preds)
    
def calc_accuracy(y_true: Type[SecretObject], y_preds: Type[SecretObject])->float:
    y_true = np.array([y_true.values]).T
    return accuracy_score(y_true, test_preds)

def calc_precision(y_true: Type[SecretObject], y_preds: Type[SecretObject], avg: str)->float:
    y_true = np.array([y_true.values]).T
    return precision_score(y_true, test_preds, average = avg)

def calc_recall(y_true: Type[SecretObject], y_preds: Type[SecretObject], avg: str)->float:
    y_true = np.array([y_true.values]).T
    return recall_score(y_true, test_preds, average = avg)

def calc_conf_mat(y_true: Type[SecretObject], y_preds: Type[SecretObject]) -> List[List[int]]:
    y_true = y_true.cpu().detach().numpy().T.astype(int)[0]
    y_preds = y_preds.T[0]
    res = confusion_matrix(y_true, y_preds)
    return res.tolist()