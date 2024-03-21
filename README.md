# 디스코드 드로잉봇  


stable diffusion을 이용한 디스코드 그림 생성 봇.  
txt2img, img2img 지원  
블로그 글: https://princesslucy.tistory.com/19

---
# Usage
1. pip install -r requirements.txt
2. Discord Developer(https://discord.com/developers/applications) 에서 봇 생성 후 `main.py`에 토큰 입력
3. `utils.py`에 openai 토큰 입력
4. 사용할 모델 `genimg.py`에 설정  
   SD모델, VAE, Lora 설정
   
   - Huggingface 모델 사용할 경우:  
     Repo 이름 그대로 사용
     
   - Civitai(https://civitai.com/) 에서 받음 safetensor or ckpt file 사용할 경우:  
     1. SD모델
     https://github.com/huggingface/diffusers/blob/main/scripts/convert_original_stable_diffusion_to_diffusers.py 에서 코드 받아서 diffusers 형태로 변환
     ```bash
     python convert_original_stable_diffusion_to_diffusers.py 
      --checkpoint_path {safetensors_path} 
      --dump_path  {save_path}
      --from_safetensors
     ```
     2. VAE
     https://github.com/huggingface/diffusers/blob/main/scripts/convert_vae_pt_to_diffusers.py 에서 코드 받아서 diffusers 형태로 변환
     ```bash
      python convert_vae_pt_to_diffusers.py 
      --vae_pt_path {vae_path} 
      --dump_path {save_path}
     ```
  5. Run
     ```python
     python main.py
     ```
  6. Discord Developer에서 만든 봇 본인 채널에 초대
---
# Example
1. txt2img
  ![image](https://github.com/pincesslucy/Discord-Drawing-bot/assets/98650288/98411199-e9c2-4fa3-88e8-01776a30f03e)

2. img2img(ghibli style)
  ![image](https://github.com/pincesslucy/Discord-Drawing-bot/assets/98650288/acbcfc18-d6fd-4b7b-b1fb-3dec566b0e5a)
