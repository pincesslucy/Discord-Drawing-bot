We will need to convert the downloaded safetensors file into another format which can be used with diffusers. For this conversion we download and use a Python script provided on HuggingFace’s GitHub repository. Note that the version of this script used should match the version of diffusers, which in this case is 0.20.0.

python convert_original_stable_diffusion_to_diffusers.py 
--checkpoint_path {safetensors_path} 
--dump_path  {save_path}
--from_safetensors

python convert_vae_pt_to_diffusers.py 
--vae_pt_path {vae_path} 
--dump_path {save_path}