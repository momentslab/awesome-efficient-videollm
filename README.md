# Awesome Efficient Video LLMs

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/momentslab/awesome-efficient-videollm/graphs/commit-activity)

A curated list of efficiency mechanisms for video large language models (VideoLLMs),
organized by **where in the pipeline the mechanism acts**: frame sampling → vision
encoder → connector & token reduction → LLM-side vision tokens.

This list accompanies our survey (link and citation to be added on publication).
Contributions welcome — see [Contributing](#contributing).

<img width="5049" height="1639" alt="EfficientVideoLLM_evolution" src="https://github.com/user-attachments/assets/579de1c4-582b-4cbf-be19-a43339a2aa8f" />

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
  - [Audio & audio-visual token compression](#audio--audio-visual-token-compression)
- [4. LLM-side Vision Tokens](#4-llm-side-vision-tokens)
  - [Decoder-layer token pruning & merging](#decoder-layer-token-pruning--merging)
  - [Visual KV-cache compression](#visual-kv-cache-compression)


## 1. Frame Sampling

### Fixed coverage sampling

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **TSN** | Temporal Segment Networks: Towards Good Practices for Deep Action Recognition | 2016 | arXiv | [paper](https://arxiv.org/abs/1608.00859) | [code](https://github.com/yjxiong/temporal-segment-networks) |

### Training-free visual summarization

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **KTS** | Category-Specific Video Summarization | 2014 | ECCV 2014 | [paper](https://doi.org/10.1007/978-3-319-10599-4_35) | — |
| **KTS-Adaptive** | Revisiting Kernel Temporal Segmentation as an Adaptive Tokenizer for Long-form Video Understanding | 2023 | arXiv | [paper](https://arxiv.org/abs/2309.11569v1) | — |
| **F2C** | From Frames to Clips: Training-free Adaptive Key Clip Selection for Long-Form Video Understanding | 2025 | arXiv | [paper](https://arxiv.org/abs/2510.02262) | — |
| **MaxInfo** | MaxInfo: A Training-Free Key-Frame Selection Method Using Maximum Volume for Enhanced Video Understanding | 2025 | arXiv | [paper](https://arxiv.org/abs/2502.03183) | [code](https://github.com/FusionBrainLab/MaxInfo) |

### Learned video-only selection

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **AdaFrame** | AdaFrame: Adaptive Frame Selection for Fast Video Recognition | 2018 | arXiv | [paper](https://arxiv.org/abs/1811.12432v2) | — |
| **MGSampler** | MGSampler: An Explainable Sampling Strategy for Video Action Recognition | 2021 | arXiv | [paper](https://arxiv.org/abs/2104.09952) | [code](https://github.com/MCG-NJU/MGSampler) |
| **PEEK** | PEEK: Picking Essential frames via Efficient Knowledge distillation | 2026 | arXiv | [paper](https://arxiv.org/abs/2605.31029) | [code](https://github.com/momentslab/peek) & [weights](https://huggingface.co/momentslab/peek) |

### Training-free relevance / diversity

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **AKS** | Adaptive Keyframe Sampling for Long Video Understanding | 2025 | CVPR 2025 | [paper](https://arxiv.org/abs/2502.21271) | [code](https://github.com/ncTimTang/AKS) |
| **AdaRD-Key** | AdaRD-key: Adaptive Relevance-Diversity Keyframe Sampling for Long-form Video Understanding | 2025 | arXiv | [paper](https://arxiv.org/abs/2510.02778) | [code](https://github.com/Xian867/AdaRD-Key) |
| **DyToK** | Less Is More, but Where? Dynamic Token Compression via LLM-Guided Keyframe Prior | 2025 | NeurIPS 2025 | [paper](https://arxiv.org/abs/2512.06866) | [code](https://github.com/yu-lin-li/DyToK) |
| **FOCUS** | FOCUS: Efficient Keyframe Selection for Long Video Understanding | 2025 | ICLR 2026 | [paper](https://arxiv.org/abs/2510.27280) | [code](https://github.com/NUS-HPC-AI-Lab/FOCUS) |
| **Q-Frame** | Q-Frame: Query-aware Frame Selection and Multi-Resolution Adaptation for Video-LLMs | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2506.22139) | [code](https://github.com/xiaomi-research/q-frame) |
| **LDDR** | LDDR: Linear-DPP-Based Dynamic-Resolution Frame Sampling for Video MLLMs | 2026 | arXiv | [paper](https://arxiv.org/abs/2605.11477) | [code](https://github.com/JingfengChen-Jay/LDDR) |

### Learned / generative query-conditioned

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **Frame-Voyager** | Frame-Voyager: Learning to Query Frames for Video Large Language Models | 2025 | ICLR 2025 | [paper](https://arxiv.org/abs/2410.03226) | — |
| **GenS** | Generative Frame Sampler for Long Video Understanding | 2025 | ACL 2025 Findings | [paper](https://arxiv.org/abs/2503.09146) | [code](https://github.com/yaolinli/GenS) & [weights](https://huggingface.co/yaolily/GenS) |
| **HFS** | HFS: Holistic Query-Aware Frame Selection for Efficient Video Reasoning | 2025 | arXiv | [paper](https://arxiv.org/abs/2512.11534) | — |
| **RL-FrameSel** | Efficient Frame Selection for Long Video Understanding via Reinforcement Learning | 2026 | CVPR 2026 | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_Efficient_Frame_Selection_for_Long_Video_Understanding_via_Reinforcement_Learning_CVPR_2026_paper.html) | — |


## 2. Vision Encoder

### Shared / unified multimodal encoders

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **MMV (TSM)** | Self-Supervised MultiModal Versatile Networks | 2020 | NeurIPS 2020 | [paper](https://arxiv.org/abs/2006.16228) | [code](https://github.com/google-deepmind/deepmind-research/tree/master/mmv) & [weights](https://github.com/google-deepmind/deepmind-research/tree/master/mmv#checkpoints) |
| **VATT** | VATT: Transformers for Multimodal Self-Supervised Learning from Raw Video, Audio and Text | 2021 | NeurIPS 2021 | [paper](https://arxiv.org/abs/2104.11178) | [code](https://github.com/google-research/google-research/tree/master/vatt) & [weights](https://github.com/google-research/google-research/tree/master/vatt#checkpoints) |
| **Meta-Transformer** | Meta-Transformer: A Unified Framework for Multimodal Learning | 2023 | arXiv | [paper](https://arxiv.org/abs/2307.10802) | [code](https://github.com/invictus717/MetaTransformer) & [weights](https://huggingface.co/kxgong/Meta-Transformer) |

### Efficient spatiotemporal backbones

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **TSM** | TSM: Temporal Shift Module for Efficient Video Understanding | 2019 | ICCV 2019 | [paper](https://arxiv.org/abs/1811.08383) | [code](https://github.com/mit-han-lab/temporal-shift-module) & [weights](https://github.com/mit-han-lab/temporal-shift-module#pretrained-models) |
| **X3D** | X3D: Expanding Architectures for Efficient Video Recognition | 2020 | CVPR 2020 | [paper](https://arxiv.org/abs/2004.04730) | [code](https://github.com/facebookresearch/SlowFast) & [weights](https://github.com/facebookresearch/SlowFast/blob/main/MODEL_ZOO.md) |
| **MViT** | Multiscale Vision Transformers | 2021 | ICCV 2021 | [paper](https://arxiv.org/abs/2104.11227) | [code](https://github.com/facebookresearch/SlowFast) |
| **MoViNet** | MoViNets: Mobile Video Networks for Efficient Video Recognition | 2021 | CVPR 2021 | [paper](https://arxiv.org/abs/2103.11511) | [code](https://github.com/tensorflow/models/tree/master/official/projects/movinet) |
| **Video Swin** | Video Swin Transformer | 2021 | arXiv | [paper](https://arxiv.org/abs/2106.13230) | [code](https://github.com/SwinTransformer/Video-Swin-Transformer) & [weights](https://github.com/SwinTransformer/Video-Swin-Transformer#results-and-models) |
| **MViTv2** | MViTv2: Improved Multiscale Vision Transformers for Classification and Detection | 2022 | CVPR 2022 | [paper](https://arxiv.org/abs/2112.01526) | [code](https://github.com/facebookresearch/mvit) |
| **UniFormer** | UniFormer: Unified Transformer for Efficient Spatiotemporal Representation Learning | 2022 | ICLR 2022 | [paper](https://arxiv.org/abs/2201.04676) | [code](https://github.com/Sense-X/UniFormer) & [weights](https://huggingface.co/Sense-X/uniformer_video) |
| **Hiera** | Hiera: A Hierarchical Vision Transformer without the Bells-and-Whistles | 2023 | ICML 2023 | [paper](https://arxiv.org/abs/2306.00989) | [code](https://github.com/facebookresearch/hiera) & [weights](https://github.com/facebookresearch/hiera#model-zoo) |
| **UniFormerV2** | UniFormerV2: Spatiotemporal Learning by Arming Image ViTs with Video UniFormer | 2023 | ICCV 2023 | [paper](https://arxiv.org/abs/2211.09552) | [code](https://github.com/OpenGVLab/UniFormerV2) & [weights](https://github.com/OpenGVLab/UniFormerV2/blob/main/MODEL_ZOO.md)|

### Linear-complexity / state-space

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **VideoMamba** | VideoMamba: State Space Model for Efficient Video Understanding | 2024 | ECCV 2024 | [paper](https://arxiv.org/abs/2403.06977) | [code](https://github.com/OpenGVLab/VideoMamba) & [weights](https://huggingface.co/OpenGVLab/VideoMamba) |
| **VideoMamba-ST** | VideoMamba: Spatio-Temporal Selective State Space Model | 2024 | ECCV 2024 | [paper](https://arxiv.org/abs/2407.08476) | — |
| **VideoMambaPro** | Snakes and Ladders: Two Steps Up for VideoMamba | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2406.19006) | [code](https://github.com/hotfinda/VideoMambaPro) & [weights](https://github.com/hotfinda/VideoMambaPro#model-weights) |

### Encoder-internal token reduction

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **ToMe** | Token Merging: Your ViT but Faster | 2023 | ICLR 2023 | [paper](https://arxiv.org/abs/2210.09461) | [code](https://github.com/facebookresearch/ToMe) |
| **ResidualViT** | ResidualViT for Efficient Temporally Dense Video Encoding | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2509.13255) | [code](https://github.com/Soldelli/residualvit) & [weights](https://github.com/Soldelli/residualvit#pretrained-checkpoints) |
| **STC** | Accelerating Streaming Video Large Language Models via Hierarchical Token Compression | 2025 | CVPR 2026 | [paper](https://arxiv.org/abs/2512.00891) | [code](https://github.com/lern-to-write/STC) |
| **EarlyTom** | EarlyTom: Early Token Compression Completes Fast Video Understanding | 2026 | CVPR 2026 | [paper](https://arxiv.org/abs/2605.30010) | [code](https://github.com/viridisGreen/EarlyTom) |

### Compressed-domain encoding

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **CoPE-VideoLM** | CoPE-VideoLM: Leveraging Codec Primitives For Efficient Video Language Modeling | 2026 | arXiv | [paper](https://arxiv.org/abs/2602.13191) | — |

### Distilled / compact vision encoders

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **TinyCLIP** | TinyCLIP: CLIP Distillation via Affinity Mimicking and Weight Inheritance | 2023 | ICCV 2023 | [paper](https://arxiv.org/abs/2309.12314) | [code](https://github.com/microsoft/Cream/tree/main/TinyCLIP) & [weights](https://huggingface.co/collections/wkcn/tinyclip-model-zoo) |
| **MobileCLIP** | MobileCLIP: Fast Image-Text Models through Multi-Modal Reinforced Training | 2024 | CVPR 2024 | [paper](https://arxiv.org/abs/2311.17049) | [code](https://github.com/apple/ml-mobileclip) & [weights](https://huggingface.co/collections/apple/mobileclip-models-datacompdr-data) |
| **MobileCLIP2** | MobileCLIP2: Improving Multi-Modal Reinforced Training | 2025 | TMLR August 2025 | [code](https://github.com/apple/ml-mobileclip) & [weights](https://huggingface.co/collections/apple/mobileclip2) | 
| **FastVLM** | FastVLM: Efficient Vision Encoding for Vision Language Models | 2025 | CVPR 2025 | [paper](https://arxiv.org/abs/2412.13303) | [code](https://github.com/apple/ml-fastvlm) & [weights](https://huggingface.co/collections/apple/fastvlm) |
| **MobileViCLIP** | MobileViCLIP: An Efficient Video-Text Model for Mobile Devices | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2508.07312) | [code](https://github.com/MCG-NJU/MobileViCLIP) & [weights](https://drive.google.com/drive/folders/1ROJYwQeO8lt4mEfNjEIAIDWj736WIQq7) |
| **LiteFrame** | LiteFrame: Efficient Vision Encoders Unlock Frame Scaling in Video LLMs | 2026 | arXiv | [paper](https://arxiv.org/abs/2605.17260) | [code](https://github.com/jjihwan/LiteFrame) |


## 3. Connector & Token Reduction

### Training-free token pruning & merging

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **Chat-UniVi** | Chat-UniVi: Unified Visual Representation Empowers Large Language Models with Image and Video Understanding | 2024 | CVPR 2024 | [paper](https://arxiv.org/abs/2311.08046) | [code](https://github.com/PKU-YuanGroup/Chat-UniVi) & [weights](https://huggingface.co/Chat-UniVi) |
| **LongVU** | LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding | 2024 | ICML 2025 | [paper](https://arxiv.org/abs/2410.17434) | [code](https://github.com/Vision-CAIR/LongVU) & [weights](https://huggingface.co/collections/Vision-CAIR/longvu) |
| **HoliTom** | HoliTom: Holistic Token Merging for Fast Video Large Language Models | 2025 | NeurIPS 2025 | [paper](https://arxiv.org/abs/2505.21334) | [code](https://github.com/cokeshao/HoliTom) |
| **LLaVA-PruMerge** | LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2403.15388) | [code](https://github.com/42Shawn/LLaVA-PruMerge) & [weights](https://huggingface.co/yuzhang/llava-prumerge-plus-vicuna-7b-v1.5-lora) |
| **PruneVid** | PruneVid: Visual Token Pruning for Efficient Video Large Language Models | 2025 | ACL Findings 2025 | [paper](https://arxiv.org/abs/2412.16117) | [code](https://github.com/Visual-AI/PruneVid) |
| **VisionZip** | VisionZip: Longer is Better but Not Necessary in Vision Language Models | 2025 | CVPR 2025 | [paper](https://arxiv.org/abs/2412.04467) | [code](https://github.com/dvlab-research/VisionZip) |
| **EchoPrune** | EchoPrune: Interpreting Redundancy as Temporal Echoes for Efficient VideoLLMs | 2026 | arXiv | [paper](https://arxiv.org/abs/2605.10050) | — |
| **FlashVID** | FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging | 2026 | ICLR 2026 | [paper](https://arxiv.org/abs/2602.08024) | [code](https://github.com/Fanziyang-v/FlashVID) |

### Query- / budget-based resampling

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **Perceiver Resampler (Flamingo)** | Flamingo: A Visual Language Model for Few-Shot Learning | 2022 | NeurIPS 2022 | [paper](https://arxiv.org/abs/2204.14198) | [(unofficial) code](https://github.com/mlfoundations/open_flamingo) & [(unofficial) weights](https://huggingface.co/openflamingo/models) |
| **LLaMA-VID** | LLaMA-VID: An Image Is Worth 2 Tokens in Large Language Models | 2023 | ECCV 2024 | [paper](https://arxiv.org/abs/2311.17043) | [code](https://github.com/dvlab-research/LLaMA-VID) & [weights](https://huggingface.co/collections/YanweiLi/llama-vid) |
| **Video-LLaMA Q-Former** | Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding | 2023 | EMNLP 2023 Demo | [paper](https://arxiv.org/abs/2306.02858) | [code](https://github.com/DAMO-NLP-SG/Video-LLaMA) & [weights](https://huggingface.co/DAMO-NLP-SG/Video-LLaMA-Series) |
| **LLaVA-Mini** | LLaVA-Mini: Efficient Image and Video Large Multimodal Models with One Vision Token | 2025 | ICLR 2025 | [paper](https://arxiv.org/abs/2501.03895) | [code](https://github.com/ictnlp/LLaVA-Mini) & [weights](https://huggingface.co/ICTNLP/llava-mini-llama-3.1-8b) |
| **VoCo-LLaMA** | VoCo-LLaMA: Towards Vision Compression with Large Language Models | 2025 | CVPR 2025 | [paper](https://arxiv.org/abs/2406.12275) | [code](https://github.com/Yxxxb/VoCo-LLaMA) |

### Spatiotemporal pooling & projection

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **PLLaVA** | PLLaVA : Parameter-free LLaVA Extension from Images to Videos for Video Dense Captioning | 2024 | arXiv | [paper](https://arxiv.org/abs/2404.16994) | [code](https://github.com/magic-research/PLLaVA) & [weights](https://huggingface.co/ermu2001/pllava-7b) |
| **SF-LLaVA** | SlowFast-LLaVA: A Strong Training-Free Baseline for Video Large Language Models | 2024 | arXiv | [paper](https://arxiv.org/abs/2407.15841) | [code](https://github.com/apple/ml-slowfast-llava) |
| **VideoLLaMA 2 (STC)** | VideoLLaMA 2: Advancing Spatial-Temporal Modeling and Audio Understanding in Video-LLMs | 2024 | arXiv | [paper](https://arxiv.org/abs/2406.07476) | [code](https://github.com/DAMO-NLP-SG/VideoLLaMA2) & [weights](https://huggingface.co/collections/DAMO-NLP-SG/videollama2) |
| **InternVL2.5 pixel-shuffle** | Expanding Performance Boundaries of Open-Source Multimodal Models with Model, Data, and Test-Time Scaling | 2025 | arXiv | [paper](https://arxiv.org/abs/2412.05271) | [code](https://github.com/OpenGVLab/InternVL) & [weights](https://huggingface.co/OpenGVLab/InternVL2_5-8B) |
| **STORM** | STORM: Token-Efficient Long Video Understanding for Multimodal LLMs | 2025 | ICCV 2025 Workshop | [paper](https://arxiv.org/abs/2503.04130) | — |

### Streaming / memory compression

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **MA-LMM** | MA-LMM: Memory-Augmented Large Multimodal Model for Long-Term Video Understanding | 2024 | CVPR 2024 | [paper](https://arxiv.org/abs/2404.05726) | [code](https://github.com/boheumd/MA-LMM) |
| **MovieChat** | MovieChat: From Dense Token to Sparse Memory for Long Video Understanding | 2024 | CVPR 2024 | [paper](https://arxiv.org/abs/2307.16449) | [code](https://github.com/rese1f/MovieChat) & [weights](https://huggingface.co/lmms-lab/MovieChat-ckpt) |
| **∞-Video** | \$\textbackslash infty\$-Video: A Training-Free Approach to Long Video Understanding via Continuous-Time Memory Consolidation | 2025 | ICML 2025 | [paper](https://arxiv.org/abs/2501.19098v2) | [code](https://github.com/deep-spin/Infinite-Video) |
| **StreamingTOM** | StreamingTOM: Streaming Token Compression for Efficient Video Understanding | 2026 | CVPR 2026 | [paper](https://arxiv.org/abs/2510.18269) | [code](https://github.com/YIGE24/StreamingTOM) |

### Audio & audio-visual token compression

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **FAVOR** | Fine-Grained Audio-Visual Joint Representations for Multimodal Large Language Models | 2023 | arXiv | [paper](https://arxiv.org/abs/2310.05863) | [code](https://github.com/BriansIDP/AudioVisualLLM) |
| **Baichuan-Omni** | Baichuan-Omni Technical Report | 2024 | arXiv | [paper](https://arxiv.org/abs/2410.08565) | [code](https://github.com/baichuan-inc/Baichuan-Omni-1.5) & [weights](https://huggingface.co/baichuan-inc/Baichuan-Omni-1d5) |
| **Qwen2-Audio pooling (audio-only antecedent)** | Qwen2-Audio Technical Report | 2024 | arXiv | [paper](https://arxiv.org/abs/2407.10759) | [code](https://github.com/QwenLM/Qwen2-Audio) & [weights](https://huggingface.co/Qwen/Qwen2-Audio-7B) |
| **video-SALMONN** | Video-SALMONN: Speech-Enhanced Audio-Visual Large Language Models | 2024 | ICML 2024 | [paper](https://arxiv.org/abs/2406.15704) | [code](https://github.com/bytedance/SALMONN/tree/videosalmonn) & [weights](https://huggingface.co/tsinghua-ee/Video-SALMONN) |
| **OmniZip** | OmniZip: Audio-Guided Dynamic Token Compression for Fast Omnimodal Large Language Models | 2025 | CVPR 2026 | [paper](https://arxiv.org/abs/2511.14582) | [code](https://github.com/KD-TAO/OmniZip) |
| **DASH** | DASH: Dynamic Audio-Driven Semantic Chunking for Efficient Omnimodal Token Compression | 2026 | ECCV 2026 | [paper](https://arxiv.org/abs/2603.15685) | [code](https://github.com/laychou666/DASH) |
| **HyperCLOVA X 8B** | HyperCLOVA X 8B Omni | 2026 | arXiv | [paper](https://arxiv.org/abs/2601.01792) | [code](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe) & [weights](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Omni-8B) |


## 4. LLM-side Vision Tokens

### Decoder-layer token pruning & merging

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **FastV** | An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models | 2024 | ECCV 2024 | [paper](https://arxiv.org/abs/2403.06764) | [code](https://github.com/pkunlp-icler/FastV) |
| **FrameFusion** | FrameFusion: Combining Similarity and Importance for Video Token Reduction on Large Vision Language Models | 2025 | ICCV 2025 | [paper](https://arxiv.org/abs/2501.01986) | [code](https://github.com/thu-nics/FrameFusion) |
| **SparseVLM** | SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference | 2025 | ICML 2025 | [paper](https://arxiv.org/abs/2410.04417) | [code](https://github.com/Gumpest/SparseVLMs) |
| **HieraVid** | HieraVid: Hierarchical Token Pruning for Fast Video Large Language Models | 2026 | arXiv | [paper](https://arxiv.org/abs/2604.01881) | — |
| **StatefulTR** | Stateful Token Reduction for Long-Video Hybrid VLMs | 2026 | arXiv | [paper](https://arxiv.org/abs/2603.00198) | — |

### Visual KV-cache compression

| Abbreviation | Title | Year | Venue | Paper | Code |
| --- | --- | :-: | :-: | :-: | :-: |
| **DyCoke** | DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models | 2025 | CVPR 2025 | [paper](https://arxiv.org/abs/2411.15024) | [code](https://github.com/KD-TAO/DyCoke) |
| **VidKV** | Plug-and-Play 1.x-Bit KV Cache Quantization for Video Large Language Models | 2025 | arXiv | [paper](https://arxiv.org/abs/2503.16257) | [code](https://github.com/KD-TAO/VidKV) |

## Contributing

Pull requests welcome. Add a method to the table of the family whose mechanism it
matches, keep rows sorted by year, and include a link to the paper (arXiv `abs`
page preferred) and to the official code when it exists.

## Citation

```bibtex
% to be added on publication
```
