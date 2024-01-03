import torch
from model_utils import set_args
import Timesnet_DANN



device = torch.device('cuda:0')
eval_mask = torch.ones(1,624).to(device)
st = torch.load('best.pth')
new_st = {key.replace("module.", ""): value for key, value in st.items()}
opt=set_args()
model = Timesnet_DANN.Model_domain(opt)
model.load_state_dict(new_st)
print("[ MODEL ] MODEL LOADED.]")
model = model.to(device)
model.eval()

print(model)