import psutil
import time

def monitor(proc):
    p = psutil.Process(proc.pid)

    cpu_samp = []
    mem_samp = []
    gpu_samp = []

    while proc.poll() is None:
        cpu_samp.append(p.cpu_percent(interval=0.5))
        mem_samp.append(p.memory_info().rss / (1024 * 1024))
        gpu_samp.append(amd_gpu())
        time.sleep(0.5)
    
    return{
        "avg_cpu": sum(cpu_samp)/len(cpu_samp) if cpu_samp else 0,
        "max_cpu": max(cpu_samp) if cpu_samp else 0,
        
        "avg_mem": sum(mem_samp)/len(mem_samp) if mem_samp else 0,
        "max_mem": max(mem_samp) if mem_samp else 0,

        "avg_gpu": sum(gpu_samp)/len(gpu_samp) if gpu_samp else 0, 
    }


def amd_gpu():
    try:
        with open("sys/class/drm/card0/device/gpu_busy_percent") as f:
            return int(f.read().strip())
    except:
        return 0