<div align="center">

# Awesome Efficient Video LLMs

**A curated list of efficiency mechanisms for video large language models (VideoLLMs),
organized by _where in the pipeline the mechanism acts_.**

<a href="https://github.com/momentslab/awesome-efficient-videollm/issues/new?template=add-paper.yml"><img alt="Add a paper" height="42" src="https://img.shields.io/badge/%E2%9E%95_Add_a_paper-2ea043?style=for-the-badge"></a>

Fill in the form and a pull request is opened for you.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/momentslab/awesome-efficient-videollm/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/momentslab/awesome-efficient-videollm?color=orange)](https://github.com/momentslab/awesome-efficient-videollm/commits/main)
[![Papers](https://img.shields.io/badge/papers-108-informational)](#contents)
[![Stars](https://img.shields.io/github/stars/momentslab/awesome-efficient-videollm?style=social)](https://github.com/momentslab/awesome-efficient-videollm/stargazers)

<img alt="Evolution of efficient VideoLLMs" src="https://github.com/user-attachments/assets/579de1c4-582b-4cbf-be19-a43339a2aa8f" />

</div>

> [!NOTE]
> This list accompanies our survey (link and citation to be added on publication).
> Contributions are welcome: a missing paper, a better category for an existing one, or an
> updated venue, code, or weights link. See [Contributing](#contributing).

## The pipeline

The four sections below follow the four cost centers of the encoder–connector–LLM pipeline.
Bracketed numbers are how many methods each stage lists.

[![Stage 1](https://img.shields.io/badge/1-Frame_Sampling_%2829%29-E4FF77?style=for-the-badge)](#1-frame-sampling)
[![Stage 2](https://img.shields.io/badge/2-Vision_Encoder_%2827%29-FF8934?style=for-the-badge)](#2-vision-encoder)
[![Stage 3](https://img.shields.io/badge/3-Connector_&_Token_Reduction_%2845%29-6342E8?style=for-the-badge)](#3-connector--token-reduction)
[![Stage 4](https://img.shields.io/badge/4-LLM--side_Vision_Tokens_%287%29-ADAAFF?style=for-the-badge)](#4-llm-side-vision-tokens)

| Stage | What it controls | Efficiency lever |
| :-- | :-- | :-- |
| **1. Frame sampling** | how many frames `T` ever reach the encoder | pick fewer, better frames |
| **2. Vision encoder** | cost per frame, and tokens produced per frame | cheaper backbones, early token reduction |
| **3. Connector** | how many of those tokens enter the LLM | pruning, merging, resampling, memory |
| **4. LLM-side** | context length `L`, prefill cost and KV-cache memory | decoder-layer pruning, KV compression |

## Contents

- [1. Frame Sampling](#1-frame-sampling)
  - [Fixed coverage sampling](#fixed-coverage-sampling)
  - [Training-free visual summarization](#training-free-visual-summarization)
  - [Learned video-only selection](#learned-video-only-selection)
  - [Training-free relevance / diversity](#training-free-relevance--diversity)
  - [Learned / generative query-conditioned](#learned--generative-query-conditioned)
- [2. Vision Encoder](#2-vision-encoder)
  - [Shared / unified multimodal encoders](#shared--unified-multimodal-encoders)
  - [Efficient spatiotemporal backbones](#efficient-spatiotemporal-backbones)
  - [Linear-complexity / state-space](#linear-complexity--state-space)
  - [Encoder-internal token reduction](#encoder-internal-token-reduction)
  - [Compressed-domain encoding](#compressed-domain-encoding)
  - [Distilled / compact vision encoders](#distilled--compact-vision-encoders)
- [3. Connector & Token Reduction](#3-connector--token-reduction)
  - [Training-free token pruning & merging](#training-free-token-pruning--merging)
  - [Query- / budget-based resampling](#query---budget-based-resampling)
  - [Spatiotemporal pooling & projection](#spatiotemporal-pooling--projection)
  - [Streaming / memory compression](#streaming--memory-compression)
  - [Audio & audiovisual token compression](#audio--audiovisual-token-compression)
- [4. LLM-side Vision Tokens](#4-llm-side-vision-tokens)
  - [Decoder-layer pruning & sparse prefill](#decoder-layer-pruning--sparse-prefill)
  - [Visual KV-cache compression](#visual-kv-cache-compression)
  - [Streaming / bounded-memory KV](#streaming--bounded-memory-kv)

## 1. Frame Sampling

![Stage 1](https://img.shields.io/badge/Stage_1-Frame_Sampling_%2829%29-E4FF77?style=flat-square)

### Fixed coverage sampling

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **TSN** | [Temporal Segment Networks: Towards Good Practices for Deep Action Recognition](https://arxiv.org/abs/1608.00859) | ![venue](https://img.shields.io/badge/ECCV-2016-1f6feb) | [![Star](https://img.shields.io/github/stars/yjxiong/temporal-segment-networks.svg?style=social&label=Star)](https://github.com/yjxiong/temporal-segment-networks) |

### Training-free visual summarization

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **KTS** | [Category-Specific Video Summarization](https://doi.org/10.1007/978-3-319-10599-4_35) | ![venue](https://img.shields.io/badge/ECCV-2014-1f6feb) | — |
| **KTS-Adaptive** | [Revisiting Kernel Temporal Segmentation as an Adaptive Tokenizer for Long-form Video Understanding](https://arxiv.org/abs/2309.11569v1) | ![venue](https://img.shields.io/badge/ICCVW-2023-1f6feb) | — |
| **F2C** | [From Frames to Clips: Training-free Adaptive Key Clip Selection for Long-Form Video Understanding](https://arxiv.org/abs/2510.02262) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | — |
| **MaxInfo** | [MaxInfo: A Training-Free Key-Frame Selection Method Using Maximum Volume for Enhanced Video Understanding](https://arxiv.org/abs/2502.03183) | ![venue](https://img.shields.io/badge/WACV-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/FusionBrainLab/MaxInfo.svg?style=social&label=Star)](https://github.com/FusionBrainLab/MaxInfo) |

### Learned video-only selection

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **AdaFrame** | [AdaFrame: Adaptive Frame Selection for Fast Video Recognition](https://arxiv.org/abs/1811.12432v2) | ![venue](https://img.shields.io/badge/CVPR-2019-1f6feb) | — |
| **MGSampler** | [MGSampler: An Explainable Sampling Strategy for Video Action Recognition](https://arxiv.org/abs/2104.09952) | ![venue](https://img.shields.io/badge/ICCV-2021-1f6feb) | [![Star](https://img.shields.io/github/stars/MCG-NJU/MGSampler.svg?style=social&label=Star)](https://github.com/MCG-NJU/MGSampler) |
| **PEEK** | [PEEK: Picking Essential frames via Efficient Knowledge distillation](https://arxiv.org/abs/2605.31029) | ![venue](https://img.shields.io/badge/BMVC-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/momentslab/peek.svg?style=social&label=Star)](https://github.com/momentslab/peek) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/momentslab/peek) |
| **AutoGaze** | [Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing](https://arxiv.org/abs/2603.12254) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/NVlabs/AutoGaze.svg?style=social&label=Star)](https://github.com/NVlabs/AutoGaze) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/bfshi/autogaze) |

### Training-free relevance / diversity

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **AKS** | [Adaptive Keyframe Sampling for Long Video Understanding](https://arxiv.org/abs/2502.21271) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/ncTimTang/AKS.svg?style=social&label=Star)](https://github.com/ncTimTang/AKS) |
| **AdaRD-Key** | [AdaRD-key: Adaptive Relevance-Diversity Keyframe Sampling for Long-form Video Understanding](https://arxiv.org/abs/2510.02778) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/Xian867/AdaRD-Key.svg?style=social&label=Star)](https://github.com/Xian867/AdaRD-Key) |
| **DyToK** | [Less Is More, but Where? Dynamic Token Compression via LLM-Guided Keyframe Prior](https://arxiv.org/abs/2512.06866) | ![venue](https://img.shields.io/badge/NeurIPS-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/yu-lin-li/DyToK.svg?style=social&label=Star)](https://github.com/yu-lin-li/DyToK) |
| **BOLT** | [BOLT: Boost Large Vision-Language Model Without Training for Long-form Video Understanding](https://arxiv.org/abs/2503.21483) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/sming256/BOLT.svg?style=social&label=Star)](https://github.com/sming256/BOLT) |
| **CoS** | [CoS: Chain-of-Shot Prompting for Long Video Understanding](https://arxiv.org/abs/2502.06428) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/lwpyh/CoS_codes.svg?style=social&label=Star)](https://github.com/lwpyh/CoS_codes) |
| **T*** | [T*: Re-thinking Temporal Search for Long-Form Video Understanding](https://arxiv.org/abs/2504.02259) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/mll-lab-nu/TStar.svg?style=social&label=Star)](https://github.com/mll-lab-nu/TStar) |
| **FOCUS** | [FOCUS: Efficient Keyframe Selection for Long Video Understanding](https://arxiv.org/abs/2510.27280) | ![venue](https://img.shields.io/badge/ICLR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/NUS-HPC-AI-Lab/FOCUS.svg?style=social&label=Star)](https://github.com/NUS-HPC-AI-Lab/FOCUS) |
| **Q-Frame** | [Q-Frame: Query-aware Frame Selection and Multi-Resolution Adaptation for Video-LLMs](https://arxiv.org/abs/2506.22139) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/xiaomi-research/q-frame.svg?style=social&label=Star)](https://github.com/xiaomi-research/q-frame) |
| **LDDR** | [LDDR: Linear-DPP-Based Dynamic-Resolution Frame Sampling for Video MLLMs](https://arxiv.org/abs/2605.11477) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | [![Star](https://img.shields.io/github/stars/JingfengChen-Jay/LDDR.svg?style=social&label=Star)](https://github.com/JingfengChen-Jay/LDDR) |
| **QCA** | [QCA: Query- and Content-Aware Keyframe Selection for Long Video Understanding](https://arxiv.org/abs/2607.00983) | ![venue](https://img.shields.io/badge/ECCV-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/hktk07/QCA.svg?style=social&label=Star)](https://github.com/hktk07/QCA) |
| **GIFT** | [GIFT: Global Irreplaceability Frame Targeting for Efficient Video Understanding](https://arxiv.org/abs/2603.25072) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | — |
| **EFS** | [Event-Anchored Frame Selection for Effective Long-Video Understanding](https://arxiv.org/abs/2603.00983) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |

### Learned / generative query-conditioned

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **Frame-Voyager** | [Frame-Voyager: Learning to Query Frames for Video Large Language Models](https://arxiv.org/abs/2410.03226) | ![venue](https://img.shields.io/badge/ICLR-2025-1f6feb) | — |
| **GenS** | [Generative Frame Sampler for Long Video Understanding](https://arxiv.org/abs/2503.09146) | ![venue](https://img.shields.io/badge/ACL_2025_Findings-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/yaolinli/GenS.svg?style=social&label=Star)](https://github.com/yaolinli/GenS) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/yaolily/GenS) |
| **ViaRL** | [ViaRL: Adaptive Temporal Grounding via Visual Iterated Amplification Reinforcement Learning](https://arxiv.org/abs/2505.15447) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | — |
| **HFS** | [HFS: Holistic Query-Aware Frame Selection for Efficient Video Reasoning](https://arxiv.org/abs/2512.11534) | ![venue](https://img.shields.io/badge/ACM_MM-2026-1f6feb) | — |
| **RL-FrameSel** | [Efficient Frame Selection for Long Video Understanding via Reinforcement Learning](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_Efficient_Frame_Selection_for_Long_Video_Understanding_via_Reinforcement_Learning_CVPR_2026_paper.html) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | — |
| **TSPO** | [TSPO: Temporal Sampling Policy Optimization for Long-form Video Language Understanding](https://arxiv.org/abs/2508.04369) | ![venue](https://img.shields.io/badge/AAAI-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/Hui-design/TSPO.svg?style=social&label=Star)](https://github.com/Hui-design/TSPO) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/hzf666/TSPO-0.4B) |
| **ReFoCUS** | [ReFoCUS: Reinforcement-guided Frame Optimization for Contextual Understanding](https://arxiv.org/abs/2506.01274) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/interlive-team/ReFoCUS.svg?style=social&label=Star)](https://github.com/interlive-team/ReFoCUS) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/interlive) |
| **VideoITG** | [VideoITG: Multimodal Video Understanding with Instructed Temporal Grounding](https://arxiv.org/abs/2507.13353) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/NVlabs/VideoITG.svg?style=social&label=Star)](https://github.com/NVlabs/VideoITG) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/nvidia/VideoITG-8B) |


## 2. Vision Encoder

![Stage 2](https://img.shields.io/badge/Stage_2-Vision_Encoder_%2827%29-FF8934?style=flat-square)

### Shared / unified multimodal encoders

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **MMV (TSM)** | [Self-Supervised MultiModal Versatile Networks](https://arxiv.org/abs/2006.16228) | ![venue](https://img.shields.io/badge/NeurIPS-2020-1f6feb) | [![Star](https://img.shields.io/github/stars/google-deepmind/deepmind-research.svg?style=social&label=Star)](https://github.com/google-deepmind/deepmind-research/tree/master/mmv) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/google-deepmind/deepmind-research/tree/master/mmv#checkpoints) |
| **VATT** | [VATT: Transformers for Multimodal Self-Supervised Learning from Raw Video, Audio and Text](https://arxiv.org/abs/2104.11178) | ![venue](https://img.shields.io/badge/NeurIPS-2021-1f6feb) | [![Star](https://img.shields.io/github/stars/google-research/google-research.svg?style=social&label=Star)](https://github.com/google-research/google-research/tree/master/vatt) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/google-research/google-research/tree/master/vatt#checkpoints) |
| **Meta-Transformer** | [Meta-Transformer: A Unified Framework for Multimodal Learning](https://arxiv.org/abs/2307.10802) | ![arXiv](https://img.shields.io/badge/arXiv-2023-b31b1b) | [![Star](https://img.shields.io/github/stars/invictus717/MetaTransformer.svg?style=social&label=Star)](https://github.com/invictus717/MetaTransformer) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/kxgong/Meta-Transformer) |

### Efficient spatiotemporal backbones

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **TSM** | [TSM: Temporal Shift Module for Efficient Video Understanding](https://arxiv.org/abs/1811.08383) | ![venue](https://img.shields.io/badge/ICCV-2019-1f6feb) | [![Star](https://img.shields.io/github/stars/mit-han-lab/temporal-shift-module.svg?style=social&label=Star)](https://github.com/mit-han-lab/temporal-shift-module) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/mit-han-lab/temporal-shift-module#pretrained-models) |
| **X3D** | [X3D: Expanding Architectures for Efficient Video Recognition](https://arxiv.org/abs/2004.04730) | ![venue](https://img.shields.io/badge/CVPR-2020-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/SlowFast.svg?style=social&label=Star)](https://github.com/facebookresearch/SlowFast) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/facebookresearch/SlowFast/blob/main/MODEL_ZOO.md) |
| **MViT** | [Multiscale Vision Transformers](https://arxiv.org/abs/2104.11227) | ![venue](https://img.shields.io/badge/ICCV-2021-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/SlowFast.svg?style=social&label=Star)](https://github.com/facebookresearch/SlowFast) |
| **MoViNet** | [MoViNets: Mobile Video Networks for Efficient Video Recognition](https://arxiv.org/abs/2103.11511) | ![venue](https://img.shields.io/badge/CVPR-2021-1f6feb) | [![Star](https://img.shields.io/github/stars/tensorflow/models.svg?style=social&label=Star)](https://github.com/tensorflow/models/tree/master/official/projects/movinet) |
| **Video Swin** | [Video Swin Transformer](https://arxiv.org/abs/2106.13230) | ![arXiv](https://img.shields.io/badge/arXiv-2021-b31b1b) | [![Star](https://img.shields.io/github/stars/SwinTransformer/Video-Swin-Transformer.svg?style=social&label=Star)](https://github.com/SwinTransformer/Video-Swin-Transformer) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/SwinTransformer/Video-Swin-Transformer#results-and-models) |
| **MViTv2** | [MViTv2: Improved Multiscale Vision Transformers for Classification and Detection](https://arxiv.org/abs/2112.01526) | ![venue](https://img.shields.io/badge/CVPR-2022-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/mvit.svg?style=social&label=Star)](https://github.com/facebookresearch/mvit) |
| **UniFormer** | [UniFormer: Unified Transformer for Efficient Spatiotemporal Representation Learning](https://arxiv.org/abs/2201.04676) | ![venue](https://img.shields.io/badge/ICLR-2022-1f6feb) | [![Star](https://img.shields.io/github/stars/Sense-X/UniFormer.svg?style=social&label=Star)](https://github.com/Sense-X/UniFormer) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/Sense-X/uniformer_video) |
| **Hiera** | [Hiera: A Hierarchical Vision Transformer without the Bells-and-Whistles](https://arxiv.org/abs/2306.00989) | ![venue](https://img.shields.io/badge/ICML-2023-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/hiera.svg?style=social&label=Star)](https://github.com/facebookresearch/hiera) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/facebookresearch/hiera#model-zoo) |
| **UniFormerV2** | [UniFormerV2: Spatiotemporal Learning by Arming Image ViTs with Video UniFormer](https://arxiv.org/abs/2211.09552) | ![venue](https://img.shields.io/badge/ICCV-2023-1f6feb) | [![Star](https://img.shields.io/github/stars/OpenGVLab/UniFormerV2.svg?style=social&label=Star)](https://github.com/OpenGVLab/UniFormerV2) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/OpenGVLab/UniFormerV2/blob/main/MODEL_ZOO.md) |
| **MoE-ViE** | [MoE-ViE: Mixture of Experts Vision Encoder for Efficient Image and Video Understanding](https://arxiv.org/abs/2608.17402) | ![venue](https://img.shields.io/badge/ECCV-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/moe_vie.svg?style=social&label=Star)](https://github.com/facebookresearch/moe_vie) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/models?search=facebook/MoEViE) |

### Linear-complexity / state-space

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **VideoMamba** | [VideoMamba: State Space Model for Efficient Video Understanding](https://arxiv.org/abs/2403.06977) | ![venue](https://img.shields.io/badge/ECCV-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/OpenGVLab/VideoMamba.svg?style=social&label=Star)](https://github.com/OpenGVLab/VideoMamba) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/OpenGVLab/VideoMamba) |
| **VideoMamba-ST** | [VideoMamba: Spatio-Temporal Selective State Space Model](https://arxiv.org/abs/2407.08476) | ![venue](https://img.shields.io/badge/ECCV-2024-1f6feb) | — |
| **VideoMambaPro** | [Snakes and Ladders: Two Steps Up for VideoMamba](https://arxiv.org/abs/2406.19006) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/hotfinda/VideoMambaPro.svg?style=social&label=Star)](https://github.com/hotfinda/VideoMambaPro) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/hotfinda/VideoMambaPro#model-weights) |

### Encoder-internal token reduction

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **ToMe** | [Token Merging: Your ViT but Faster](https://arxiv.org/abs/2210.09461) | ![venue](https://img.shields.io/badge/ICLR-2023-1f6feb) | [![Star](https://img.shields.io/github/stars/facebookresearch/ToMe.svg?style=social&label=Star)](https://github.com/facebookresearch/ToMe) |
| **ResidualViT** | [ResidualViT for Efficient Temporally Dense Video Encoding](https://arxiv.org/abs/2509.13255) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/Soldelli/residualvit.svg?style=social&label=Star)](https://github.com/Soldelli/residualvit) [![Weights](https://img.shields.io/badge/Weights-link-181717?logo=github&logoColor=white)](https://github.com/Soldelli/residualvit#pretrained-checkpoints) |
| **STC** | [Accelerating Streaming Video Large Language Models via Hierarchical Token Compression](https://arxiv.org/abs/2512.00891) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/lern-to-write/STC.svg?style=social&label=Star)](https://github.com/lern-to-write/STC) |
| **EarlyTom** | [EarlyTom: Early Token Compression Completes Fast Video Understanding](https://arxiv.org/abs/2605.30010) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/viridisGreen/EarlyTom.svg?style=social&label=Star)](https://github.com/viridisGreen/EarlyTom) |

### Compressed-domain encoding

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **CoPE-VideoLM** | [CoPE-VideoLM: Leveraging Codec Primitives For Efficient Video Language Modeling](https://arxiv.org/abs/2602.13191) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |

### Distilled / compact vision encoders

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **TinyCLIP** | [TinyCLIP: CLIP Distillation via Affinity Mimicking and Weight Inheritance](https://arxiv.org/abs/2309.12314) | ![venue](https://img.shields.io/badge/ICCV-2023-1f6feb) | [![Star](https://img.shields.io/github/stars/microsoft/Cream.svg?style=social&label=Star)](https://github.com/microsoft/Cream/tree/main/TinyCLIP) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/wkcn/tinyclip-model-zoo) |
| **MobileCLIP** | [MobileCLIP: Fast Image-Text Models through Multi-Modal Reinforced Training](https://arxiv.org/abs/2311.17049) | ![venue](https://img.shields.io/badge/CVPR-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/apple/ml-mobileclip.svg?style=social&label=Star)](https://github.com/apple/ml-mobileclip) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/apple/mobileclip-models-datacompdr-data) |
| **MobileCLIP2** | [MobileCLIP2: Improving Multi-Modal Reinforced Training](https://arxiv.org/abs/2508.20691) | ![venue](https://img.shields.io/badge/TMLR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/apple/ml-mobileclip.svg?style=social&label=Star)](https://github.com/apple/ml-mobileclip) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/apple/mobileclip2) |
| **FastVLM** | [FastVLM: Efficient Vision Encoding for Vision Language Models](https://arxiv.org/abs/2412.13303) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/apple/ml-fastvlm.svg?style=social&label=Star)](https://github.com/apple/ml-fastvlm) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/apple/fastvlm) |
| **MobileViCLIP** | [MobileViCLIP: An Efficient Video-Text Model for Mobile Devices](https://arxiv.org/abs/2508.07312) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/MCG-NJU/MobileViCLIP.svg?style=social&label=Star)](https://github.com/MCG-NJU/MobileViCLIP) [![Weights](https://img.shields.io/badge/Weights-Drive-4285F4?logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1ROJYwQeO8lt4mEfNjEIAIDWj736WIQq7) |
| **LiteFrame** | [LiteFrame: Efficient Vision Encoders Unlock Frame Scaling in Video LLMs](https://arxiv.org/abs/2605.17260) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | [![Star](https://img.shields.io/github/stars/jjihwan/LiteFrame.svg?style=social&label=Star)](https://github.com/jjihwan/LiteFrame) |


## 3. Connector & Token Reduction

![Stage 3](https://img.shields.io/badge/Stage_3-Connector_&_Token_Reduction_%2845%29-6342E8?style=flat-square)

### Training-free token pruning & merging

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **Chat-UniVi** | [Chat-UniVi: Unified Visual Representation Empowers Large Language Models with Image and Video Understanding](https://arxiv.org/abs/2311.08046) | ![venue](https://img.shields.io/badge/CVPR-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/PKU-YuanGroup/Chat-UniVi.svg?style=social&label=Star)](https://github.com/PKU-YuanGroup/Chat-UniVi) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/Chat-UniVi) |
| **LongVU** | [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](https://arxiv.org/abs/2410.17434) | ![venue](https://img.shields.io/badge/ICML-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/Vision-CAIR/LongVU.svg?style=social&label=Star)](https://github.com/Vision-CAIR/LongVU) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/Vision-CAIR/longvu) |
| **HoliTom** | [HoliTom: Holistic Token Merging for Fast Video Large Language Models](https://arxiv.org/abs/2505.21334) | ![venue](https://img.shields.io/badge/NeurIPS-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/cokeshao/HoliTom.svg?style=social&label=Star)](https://github.com/cokeshao/HoliTom) |
| **LLaVA-PruMerge** | [LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models](https://arxiv.org/abs/2403.15388) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/42Shawn/LLaVA-PruMerge.svg?style=social&label=Star)](https://github.com/42Shawn/LLaVA-PruMerge) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/yuzhang/llava-prumerge-plus-vicuna-7b-v1.5-lora) |
| **PruneVid** | [PruneVid: Visual Token Pruning for Efficient Video Large Language Models](https://arxiv.org/abs/2412.16117) | ![venue](https://img.shields.io/badge/ACL_Findings-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/Visual-AI/PruneVid.svg?style=social&label=Star)](https://github.com/Visual-AI/PruneVid) |
| **VisionZip** | [VisionZip: Longer is Better but Not Necessary in Vision Language Models](https://arxiv.org/abs/2412.04467) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/dvlab-research/VisionZip.svg?style=social&label=Star)](https://github.com/dvlab-research/VisionZip) |
| **FastVID** | [FastVID: Dynamic Density Pruning for Fast Video Large Language Models](https://arxiv.org/abs/2503.11187) | ![venue](https://img.shields.io/badge/NeurIPS-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/LunarShen/FastVID.svg?style=social&label=Star)](https://github.com/LunarShen/FastVID) |
| **STTM** | [Multi-Granular Spatio-Temporal Token Merging for Training-Free Acceleration of Video LLMs](https://arxiv.org/abs/2507.07990) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/HYUNJS/STTM.svg?style=social&label=Star)](https://github.com/HYUNJS/STTM) |
| **LLaVA-Scissor** | [LLaVA-Scissor: Token Compression with Semantic Connected Components for Video LLMs](https://arxiv.org/abs/2506.21862) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/HumanMLLM/LLaVA-Scissor.svg?style=social&label=Star)](https://github.com/HumanMLLM/LLaVA-Scissor) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/BBBBCHAN/LLaVA-Scissor-baseline-7B) |
| **VidCom²** | [Video Compression Commander: Plug-and-Play Inference Acceleration for Video Large Language Models](https://arxiv.org/abs/2505.14454) | ![venue](https://img.shields.io/badge/EMNLP-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/xuyang-liu16/VidCom2.svg?style=social&label=Star)](https://github.com/xuyang-liu16/VidCom2) |
| **EchoPrune** | [EchoPrune: Interpreting Redundancy as Temporal Echoes for Efficient VideoLLMs](https://arxiv.org/abs/2605.10050) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |
| **FlashVID** | [FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging](https://arxiv.org/abs/2602.08024) | ![venue](https://img.shields.io/badge/ICLR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/Fanziyang-v/FlashVID.svg?style=social&label=Star)](https://github.com/Fanziyang-v/FlashVID) |
| **KTV** | [KTV: Keyframes and Key Tokens Selection for Efficient Training-Free Video LLMs](https://arxiv.org/abs/2602.03615) | ![venue](https://img.shields.io/badge/AAAI-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/hktk07/KTV.svg?style=social&label=Star)](https://github.com/hktk07/KTV) |
| **MMG-Vid** | [MMG-Vid: Maximizing Marginal Gains at Segment-level and Token-level for Efficient Video LLMs](https://arxiv.org/abs/2508.21044) | ![venue](https://img.shields.io/badge/AAAI-2026-1f6feb) | — |
| **OTT-Vid** | [OTT-Vid: Optimal Transport Temporal Token Compression for Video Large Language Models](https://arxiv.org/abs/2605.11803) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | [![Star](https://img.shields.io/github/stars/minseokii/OTT-Vid.svg?style=social&label=Star)](https://github.com/minseokii/OTT-Vid) |
| **DynaTok** | [DynaTok: Temporally Adaptive and Positional Bias-Aware Token Compression for Video-LLMs](https://arxiv.org/abs/2605.19322) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |
| **InfoMerge** | [InfoMerge: Information-aware Token Compression for Efficient Video Large Language Models](https://arxiv.org/abs/2606.02161) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |
| **ForestPrune** | [ForestPrune: High-ratio Visual Token Compression for Video Multimodal Large Language Models via Spatial-Temporal Forest Modeling](https://arxiv.org/abs/2603.22911) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | — |
| **MeToM** | [MeToM: Metadata-Guided Token Merging for Efficient Video LLMs](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_MeToM_Metadata-Guided_Token_Merging_for_Efficient_Video_LLMs_CVPR_2026_paper.pdf) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | — |

### Query- / budget-based resampling

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **Perceiver Resampler (Flamingo)** | [Flamingo: A Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198) | ![venue](https://img.shields.io/badge/NeurIPS-2022-1f6feb) | [![Code](https://img.shields.io/badge/Code-unofficial-lightgrey?logo=github)](https://github.com/mlfoundations/open_flamingo) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights_%28unofficial%29-FFD21E)](https://huggingface.co/openflamingo/models) |
| **LLaMA-VID** | [LLaMA-VID: An Image Is Worth 2 Tokens in Large Language Models](https://arxiv.org/abs/2311.17043) | ![venue](https://img.shields.io/badge/ECCV-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/dvlab-research/LLaMA-VID.svg?style=social&label=Star)](https://github.com/dvlab-research/LLaMA-VID) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/YanweiLi/llama-vid) |
| **Video-LLaMA Q-Former** | [Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding](https://arxiv.org/abs/2306.02858) | ![venue](https://img.shields.io/badge/EMNLP_2023_Demo-2023-1f6feb) | [![Star](https://img.shields.io/github/stars/DAMO-NLP-SG/Video-LLaMA.svg?style=social&label=Star)](https://github.com/DAMO-NLP-SG/Video-LLaMA) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/DAMO-NLP-SG/Video-LLaMA-Series) |
| **BLIP-3-Video** | [xGen-MM-Vid (BLIP-3-Video): You Only Need 32 Tokens to Represent a Video Even in VLMs](https://arxiv.org/abs/2410.16267) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/Salesforce/xgen-mm-vid-phi3-mini-r-v1.5-128tokens-8frames) |
| **VidCompress** | [VidCompress: Memory-Enhanced Temporal Compression for Video Understanding in Large Language Models](https://arxiv.org/abs/2410.11417) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | — |
| **LLaVA-Mini** | [LLaVA-Mini: Efficient Image and Video Large Multimodal Models with One Vision Token](https://arxiv.org/abs/2501.03895) | ![venue](https://img.shields.io/badge/ICLR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/ictnlp/LLaVA-Mini.svg?style=social&label=Star)](https://github.com/ictnlp/LLaVA-Mini) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/ICTNLP/llava-mini-llama-3.1-8b) |
| **VoCo-LLaMA** | [VoCo-LLaMA: Towards Vision Compression with Large Language Models](https://arxiv.org/abs/2406.12275) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/Yxxxb/VoCo-LLaMA.svg?style=social&label=Star)](https://github.com/Yxxxb/VoCo-LLaMA) |
| **Quicksviewer** | [Quicksviewer: An LMM for Efficient Video Understanding via Reinforced Compression of Video Cubes](https://arxiv.org/abs/2504.15270v1) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/quicksviewer/quicksviewer.svg?style=social&label=Star)](https://github.com/quicksviewer/quicksviewer) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/qijithu/quicksviewer) |

### Spatiotemporal pooling & projection

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **PLLaVA** | [PLLaVA : Parameter-free LLaVA Extension from Images to Videos for Video Dense Captioning](https://arxiv.org/abs/2404.16994) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Star](https://img.shields.io/github/stars/magic-research/PLLaVA.svg?style=social&label=Star)](https://github.com/magic-research/PLLaVA) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/ermu2001/pllava-7b) |
| **SF-LLaVA** | [SlowFast-LLaVA: A Strong Training-Free Baseline for Video Large Language Models](https://arxiv.org/abs/2407.15841) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Star](https://img.shields.io/github/stars/apple/ml-slowfast-llava.svg?style=social&label=Star)](https://github.com/apple/ml-slowfast-llava) |
| **VideoLLaMA 2 (STC)** | [VideoLLaMA 2: Advancing Spatial-Temporal Modeling and Audio Understanding in Video-LLMs](https://arxiv.org/abs/2406.07476) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Star](https://img.shields.io/github/stars/DAMO-NLP-SG/VideoLLaMA2.svg?style=social&label=Star)](https://github.com/DAMO-NLP-SG/VideoLLaMA2) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/DAMO-NLP-SG/videollama2) |
| **InternVL2.5 pixel-shuffle** | [Expanding Performance Boundaries of Open-Source Multimodal Models with Model, Data, and Test-Time Scaling](https://arxiv.org/abs/2412.05271) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/OpenGVLab/InternVL.svg?style=social&label=Star)](https://github.com/OpenGVLab/InternVL) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/OpenGVLab/InternVL2_5-8B) |
| **STORM** | [STORM: Token-Efficient Long Video Understanding for Multimodal LLMs](https://arxiv.org/abs/2503.04130) | ![venue](https://img.shields.io/badge/ICCV_2025_Workshop-2025-1f6feb) | — |
| **NVILA** | [NVILA: Efficient Frontier Visual Language Models](https://arxiv.org/abs/2412.04468) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/NVlabs/VILA.svg?style=social&label=Star)](https://github.com/NVlabs/VILA) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/collections/Efficient-Large-Model/nvila) |
| **PVC** | [PVC: Progressive Visual Token Compression for Unified Image and Video Processing in Large Vision-Language Models](https://arxiv.org/abs/2412.09613) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/OpenGVLab/PVC.svg?style=social&label=Star)](https://github.com/OpenGVLab/PVC) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/OpenGVLab/PVC-InternVL2-8B) |

### Streaming / memory compression

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **MA-LMM** | [MA-LMM: Memory-Augmented Large Multimodal Model for Long-Term Video Understanding](https://arxiv.org/abs/2404.05726) | ![venue](https://img.shields.io/badge/CVPR-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/boheumd/MA-LMM.svg?style=social&label=Star)](https://github.com/boheumd/MA-LMM) |
| **MovieChat** | [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](https://arxiv.org/abs/2307.16449) | ![venue](https://img.shields.io/badge/CVPR-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/rese1f/MovieChat.svg?style=social&label=Star)](https://github.com/rese1f/MovieChat) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/lmms-lab/MovieChat-ckpt) |
| **∞-Video** | [∞-Video: A Training-Free Approach to Long Video Understanding via Continuous-Time Memory Consolidation](https://arxiv.org/abs/2501.19098v2) | ![venue](https://img.shields.io/badge/ICML-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/deep-spin/Infinite-Video.svg?style=social&label=Star)](https://github.com/deep-spin/Infinite-Video) |
| **StreamingTOM** | [StreamingTOM: Streaming Token Compression for Efficient Video Understanding](https://arxiv.org/abs/2510.18269) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/YIGE24/StreamingTOM.svg?style=social&label=Star)](https://github.com/YIGE24/StreamingTOM) |

### Audio & audiovisual token compression

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **FAVOR** | [Fine-Grained Audio-Visual Joint Representations for Multimodal Large Language Models](https://arxiv.org/abs/2310.05863) | ![arXiv](https://img.shields.io/badge/arXiv-2023-b31b1b) | [![Star](https://img.shields.io/github/stars/BriansIDP/AudioVisualLLM.svg?style=social&label=Star)](https://github.com/BriansIDP/AudioVisualLLM) |
| **Baichuan-Omni** | [Baichuan-Omni Technical Report](https://arxiv.org/abs/2410.08565) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Star](https://img.shields.io/github/stars/baichuan-inc/Baichuan-Omni-1.5.svg?style=social&label=Star)](https://github.com/baichuan-inc/Baichuan-Omni-1.5) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/baichuan-inc/Baichuan-Omni-1d5) |
| **Qwen2-Audio pooling (audio-only antecedent)** | [Qwen2-Audio Technical Report](https://arxiv.org/abs/2407.10759) | ![arXiv](https://img.shields.io/badge/arXiv-2024-b31b1b) | [![Star](https://img.shields.io/github/stars/QwenLM/Qwen2-Audio.svg?style=social&label=Star)](https://github.com/QwenLM/Qwen2-Audio) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/Qwen/Qwen2-Audio-7B) |
| **video-SALMONN** | [Video-SALMONN: Speech-Enhanced Audio-Visual Large Language Models](https://arxiv.org/abs/2406.15704) | ![venue](https://img.shields.io/badge/ICML-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/bytedance/SALMONN.svg?style=social&label=Star)](https://github.com/bytedance/SALMONN/tree/videosalmonn) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/tsinghua-ee/Video-SALMONN) |
| **OmniZip** | [OmniZip: Audio-Guided Dynamic Token Compression for Fast Omnimodal Large Language Models](https://arxiv.org/abs/2511.14582) | ![venue](https://img.shields.io/badge/CVPR-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/KD-TAO/OmniZip.svg?style=social&label=Star)](https://github.com/KD-TAO/OmniZip) |
| **DASH** | [DASH: Dynamic Audio-Driven Semantic Chunking for Efficient Omnimodal Token Compression](https://arxiv.org/abs/2603.15685) | ![venue](https://img.shields.io/badge/ECCV-2026-1f6feb) | [![Star](https://img.shields.io/github/stars/laychou666/DASH.svg?style=social&label=Star)](https://github.com/laychou666/DASH) |
| **HyperCLOVA X 8B** | [HyperCLOVA X 8B Omni](https://arxiv.org/abs/2601.01792) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | [![Star](https://img.shields.io/github/stars/NAVER-Cloud-HyperCLOVA-X/OmniServe.svg?style=social&label=Star)](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe) [![Weights](https://img.shields.io/badge/%F0%9F%A4%97_Weights-FFD21E)](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Omni-8B) |


## 4. LLM-side Vision Tokens

![Stage 4](https://img.shields.io/badge/Stage_4-LLM--side_Vision_Tokens_%287%29-ADAAFF?style=flat-square)

### Decoder-layer pruning & sparse prefill

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **FastV** | [An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models](https://arxiv.org/abs/2403.06764) | ![venue](https://img.shields.io/badge/ECCV-2024-1f6feb) | [![Star](https://img.shields.io/github/stars/pkunlp-icler/FastV.svg?style=social&label=Star)](https://github.com/pkunlp-icler/FastV) |
| **FrameFusion** | [FrameFusion: Combining Similarity and Importance for Video Token Reduction on Large Vision Language Models](https://arxiv.org/abs/2501.01986) | ![venue](https://img.shields.io/badge/ICCV-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/thu-nics/FrameFusion.svg?style=social&label=Star)](https://github.com/thu-nics/FrameFusion) |
| **SparseVLM** | [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](https://arxiv.org/abs/2410.04417) | ![venue](https://img.shields.io/badge/ICML-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/Gumpest/SparseVLMs.svg?style=social&label=Star)](https://github.com/Gumpest/SparseVLMs) |
| **HieraVid** | [HieraVid: Hierarchical Token Pruning for Fast Video Large Language Models](https://arxiv.org/abs/2604.01881) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |
| **StatefulTR** | [Stateful Token Reduction for Long-Video Hybrid VLMs](https://arxiv.org/abs/2603.00198) | ![arXiv](https://img.shields.io/badge/arXiv-2026-b31b1b) | — |

### Visual KV-cache compression

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |
| **DyCoke** | [DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models](https://arxiv.org/abs/2411.15024) | ![venue](https://img.shields.io/badge/CVPR-2025-1f6feb) | [![Star](https://img.shields.io/github/stars/KD-TAO/DyCoke.svg?style=social&label=Star)](https://github.com/KD-TAO/DyCoke) |
| **VidKV** | [Plug-and-Play 1.x-Bit KV Cache Quantization for Video Large Language Models](https://arxiv.org/abs/2503.16257) | ![arXiv](https://img.shields.io/badge/arXiv-2025-b31b1b) | [![Star](https://img.shields.io/github/stars/KD-TAO/VidKV.svg?style=social&label=Star)](https://github.com/KD-TAO/VidKV) |

### Streaming / bounded-memory KV

| Method | Title | Venue | Code & Weights |
| --- | --- | :-: | :-: |

## Contributing

**By issue form.** [Open an "Add a paper" issue](https://github.com/momentslab/awesome-efficient-videollm/issues/new?template=add-paper.yml)
and give the abbreviation, title, links, venue, and the family it belongs to. A bot opens the pull
request with the row already formatted. You need no fork, no markdown, and no local tooling.

**By pull request.** Edit the table of the family whose mechanism the method matches. Write the row
in whatever shape is convenient. This one is fine:

```markdown
| **Abbrev** | Full title | 2026 | ICLR 2026 | [paper](paper-url) | [code](repo-url) & [weights](weights-url) |
```

After the merge, a bot rewrites the row into the badge form the tables use, regenerates the
contents list, and updates the per-stage and total counts. You do not need to match the badge
syntax or correct the counts yourself.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

```bibtex
% to be added on publication
```

## Contributors

<a href="https://github.com/momentslab/awesome-efficient-videollm/graphs/contributors">
  <img alt="Contributors" src="https://contrib.rocks/image?repo=momentslab/awesome-efficient-videollm" />
</a>

<div align="right"><a href="#awesome-efficient-video-llms">⬆ Back to top</a></div>
