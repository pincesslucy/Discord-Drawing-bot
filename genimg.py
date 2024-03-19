from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, AutoencoderKL, AutoPipelineForImage2Image
import torch
import random
import transformers
from PIL import Image

def gen_img(prompt):
    RANDOM_SEED = random.randint(0, 1000000)

    text_encoder = transformers.CLIPTextModel.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        subfolder = "text_encoder",
        num_hidden_layers = 12 - (2 - 1),
        torch_dtype = torch.float16
    )

    pipeline = StableDiffusionPipeline.from_pretrained(
        "./models/majicmix", 
        torch_dtype=torch.float16, 
        safety_checker=None, 
        use_safetensors=True,
        text_encoder=text_encoder
    ).to("cuda")

    vae = AutoencoderKL.from_pretrained("./vae/ema", torch_dtype=torch.float16).to("cuda")

    pipeline.schedule = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)
    pipeline.load_lora_weights(".", weight_name="./lora/add_detail.safetensors")
    pipeline.vae = vae

    prompts = "(((masterpiece))), realistic, best quality, ultra high res, (photorealistic:1.4) ," + prompt

    negative_prompt = "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans"

    generator = torch.Generator(device="cuda").manual_seed(RANDOM_SEED)

    new_image = pipeline(
        prompt=prompts, 
        negative_prompt=negative_prompt,  
        guidance_scale=8, 
        generator=generator, 
        num_inference_steps=30,
        width=768,
        height=768,
    ).images[0]

    new_image.save(f"./images/{RANDOM_SEED}.png")
    return f"./images/{RANDOM_SEED}.png"

# gen_img("flying castle, ghibli, anime, sky, clouds, fantasy, dream, dreamy")

def img_to_img(path, prompt):
    RANDOM_SEED = random.randint(0, 1000000)

    pipeline = AutoPipelineForImage2Image.from_pretrained(
        "stablediffusionapi/anything-v5",
        torch_dtype=torch.float16,
        safety_checker=None
    ).to("cuda")

    vae = AutoencoderKL.from_pretrained("./vae/anime", torch_dtype=torch.float16).to("cuda")
    pipeline.schedule = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)
    pipeline.load_lora_weights(".", weight_name="./lora/ghibli_style_offset.safetensors")
    pipeline.vae = vae


    prompt = "(((masterpiece))), best quality, ghibli style, " + prompt

    negative_prompt = "(worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans"

    image = Image.open(path).convert("RGB")
    generator = torch.Generator(device="cuda").manual_seed(RANDOM_SEED)

    new_image = pipeline(prompt=prompt, negative_prompt=negative_prompt, image=image, strength=0.6, guidance_scale=8, generator=generator, num_inference_steps=30).images[0]

    new_image.save(f"./images/{RANDOM_SEED}.png")
    return f"./images/{RANDOM_SEED}.png"