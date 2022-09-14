import pandas as pd
import inspect

module = pd.Series
df_dict = module.__dict__

#for key in df_dict.keys():
#    if not key.startswith("_") and inspect.isfunction(df_dict[key]):
#        sig = inspect.signature(df_dict[key])
#        print("def " + df_dict[key].__name__ + sig.__str__() + ":")
#        funcargs = list(sig.parameters.keys())[1:]
##        funcargs = "(" + str(funcargs)[1:-1].replace("'", "") + ")"
#        print("    ans = self.series." + df_dict[key].__name__ + funcargs)
#        print()

for key in df_dict.keys():
    if not key.startswith("_") and not inspect.isfunction(df_dict[key]):
        print(key)
        
