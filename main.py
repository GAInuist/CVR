import argparse
import os

parser = argparse.ArgumentParser()

# ############################  segmentation setting  #############################
parser.add_argument('--virtual_image_path', default='./dataset/Sea/images/validation',
                    type=str, help='the path of the virtual image')
# parser.add_argument('--segmentation_model_path', default='./SAM/experiment/model/semantic_sam/model.pth',
#                     type=str, help='the path of the segmentation model')
# parser.add_argument('--segmentation_results_path', default='sam_results',
#                     type=str, help='the path of the segmentation results')

############################  diffusion model setting  #############################
parser.add_argument('--diffusion_model_path', default='./SDM/OUTPUT/save/seas_256-300000-l1.pt',
                    type=str, help='the path of the diffusion model')
parser.add_argument('--generated_images_path', default='output',
                    type=str, help='the path of the generated images')
parser.add_argument('--num_samples', default='3',
                    type=int, help='the number of generated images')

############################  super resolution setting  #############################
parser.add_argument('--super_resolution_option', default='./HAT-main/options/test/HAT_SRx4_ImageNet-LR-org.yml',
                    type=str, help='the option of super resolution')

args = parser.parse_args()

if __name__ == '__main__':
    # #### segmentation setting ####
    virtual_image_path = args.virtual_image_path
    # segmentation_model_path = args.segmentation_model_path
    # segmentation_results_path = args.segmentation_results_path

    #### diffusion model setting ####
    diffusion_model_path = args.diffusion_model_path
    generated_images_path = args.generated_images_path
    num_samples = args.num_samples

    #### super resolution setting ####
    super_resolution_option = args.super_resolution_option

    #### run ####
    os.system(f'python SAM/predict.py \
              --cuda_visible_devices 0 \
              --img_path {virtual_image_path} \
              ')
    print('\nFinished segmenting\n')

    sdm_dataset = './dataset/Sea'
    os.system(f'CUDA_VISIBLE_DEVICE=0 python SDM/image_sample.py \
    --data_dir {sdm_dataset} \
    --dataset_mode seas --attention_resolutions 32,16,8 \
    --diffusion_steps 1000 \
    --image_size 256 \
    --learn_sigma True \
    --noise_schedule linear \
    --num_channels 256 \
    --num_head_channels 64 \
    --num_res_blocks 2 \
    --resblock_updown True \
    --use_fp16 True \
    --use_scale_shift_norm True \
    --num_classes 5 \
    --class_cond True \
    --no_instance True \
    --batch_size 1 \
    --num_samples {num_samples-1} \
    --model_path {diffusion_model_path} \
    --results_path {generated_images_path} \
    --s 1.5\
    # --timestep_respacing ddim100\
    # --use_ddim True'\
    )
    print('\nFinished generating images\n')

    os.system(f'CUDA_VISIBLE_DEVICE=0,1 python ./HAT-main/hat/test.py \
    -opt {super_resolution_option}')
    print('\nFinished super resolution\n')

