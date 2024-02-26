import time
import torch
import os
import tempfile
from Model_unet import UNet


def get_model_size_in_MB(model):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    torch.save(model.state_dict(), temp.name)
    size_MB = os.path.getsize(temp.name) / (1024 * 1024)
    os.remove(temp.name)
    return size_MB


def get_model_metrics(model, input_tensor):
    from thop import profile
    flops, params = profile(model, inputs=(input_tensor,))
    metrics = {
        "FLOPs": f"{flops / 1e6:.2f} MFLOPs",
        "Parameters": f"{params / 1e6:.2f}M",
        "Model Size": f"{get_model_size_in_MB(model):.2f} MB"
    }
    return metrics


def test_inference_speed(model, input_tensor):
    time_list=[]
    model.eval()
    with torch.no_grad():
        for _ in range(100):
            start_time = time.time()
            model(input_tensor)
            end_time = time.time()
            time_list.append(end_time-start_time)
    avg_time = sum(time_list[:50])*1000/len(time_list[:50])
    return avg_time

if __name__ == '__main__':
    model = UNet(in_channels=3, num_classes=4 + 1, base_c=32)
    model.eval()
    input_tensor = torch.rand(1,3,120, 120)
    print(input_tensor.shape)
    try:
        metrics = get_model_metrics(model, input_tensor)
        print(f"Model metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(e)

    inference_time = test_inference_speed(model, input_tensor)
    print(f"Inference time: {inference_time:.2f} ms")
