import torch

class GradCAM:
    def __init__(self,
                 model,
                 target_layers,
                 reshape_transform=None,
                 use_cuda=False):
        self.model = model.eval()
        self.target_layers = target_layers
        self.reshape_transform = reshape_transform
        self.use_cuda = use_cuda
        if self.use_cuda:
            self.model = self.model.cuda()
        else:
            pass
        self.activations_and_grads = ActivationsAndGradients(self.model, 
                                     target_layers, reshape_transform)
        # 实例化了ActivationsAndGradients类

class ActivationsAndGradients:
    # 自动调用__call__()函数，获取正向传播的特征层A和反向传播的梯度A'
    def __init__(self, model, target_layers, reshape_transform): 

        # 传入模型参数，申明特征层的存储空间（self.activations）
        # 和回传梯度的存储空间（self.gradients）
        self.model = model
        self.gradients = []
        self.activations = []
        self.reshape_transform = reshape_transform
        self.handles = []

        # 注意，上文指明目标网络层是是用列表存储的（target_layers = [model.down4]）
        # 源码设计的可以得到多层cam图
        # 这里注册了一个前向传播的钩子函数“register_forward_hook()”，其作用是
        # 在不改变网络结构的情况下获取某一层的输出，也就是获取正向传播的特征层
        for target_layer in target_layers:
            self.handles.append(
                target_layer.register_forward_hook(
                    self.save_activation
                )
            )
        
        # hasattr(object,name)返回值:如果对象有该属性返回True,否则返回False
        # 其作用是判断当前环境中是否存在该函数（解决版本不匹配的问题）
        if hasattr(target_layer, 'register_full_backward_hook'):
            self.handles.append(
                target_layer.register_full_backward_hook(self.save_gradient))
        else:
            # 注册反向传播的钩子函数“register_backward_hook”，用于存储反向传播过程中梯度图
            self.handles.append(
                target_layer.register_backward_hook(self.save_gradient))
    
    # 官方API文档对于register_forward_hook()函数有着类似的用法，
    # self.activations中存储了正向传播过程中的特征层
    def save_activation(self, module, input, output):
        activation = output
        if self.reshape_transform is not None:
            activation = self.reshape_transform(activation)
        self.activations.append(activation.cpu().detach())
    
    # 与上述类似，只不过save_gradient()存储梯度信息，值得注意的是self.gradients的存储顺序
    def save_gradient(self, model, grad_input, grad_output):
        grad = grad_output[0]
        if self.reshape_transform is not None:
            grad = self.reshape_transform(grad)
        self.gradients = [grad.cpu().detach()] + self.gradients 
        # 反向传播的梯度A’放在最前，目的是与特征层顺序一致

    def __call__(self, x):
        # 自动调用，会self.model(x)开始正向传播，注意此时并没有反向传播的操作
        self.gradients = []
        self.activations = []
        return self.model(x)

    def release(self):
        for handle in self.handles:
            handle.remove()
            # handle要及时移除掉，不然会占用过多内存