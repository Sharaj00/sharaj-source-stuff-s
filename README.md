# sharaj source stuff's

a set of vibe-coded scripts for working with Source Engine models in Blender 4.0+ (not guaranteed to work on older versions)

## Features

- **[Proportion Trick](https://github.com/sksh70/proportion_trick_script)**  
  Launch directly from the N-panel. Just select a suitable armature and press the button

- **Bone Tools**  
  Some little but usefull scripts for better bone operating
  - Deselect all ValveBiped bones
  - Auto-rotate jiggle bones to face -Z for correct physics behavior
  - Point jiggle bones at the 3D cursor (for pitch-limited config)
  - Generate LOD merge configuration

- **VMT Tools**  
  Create material files based on `Principled BSDF` settings:
  - Base color and normal maps
  - Emission enabling (WIP)
  - Fake gloss using `phong` (WIP)

- **Eye Tools (WIP)**  
  - Generate configuration for eyes based on pasted XYZ coordinates for L/R eye

- **QC Tools (WIP)**  
  Some useless utilities for generating QC files

## TODO

- Better vmt generation with lot of options to enable through panel
- Generate QC example for playermodel or prop, with bodygroups based on scene collections
- Better jiggle bones config generaion, or abandoning it in favor of [this](https://github.com/Jakobg1215/srcprocbones) addon
- Advanced eye configs with eyelid configuration and preview how it will looks directly in Blender
