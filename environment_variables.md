# Environment variables

## Table of Contents

- [Introduction](#introduction)
- [Variables](#variables)

## Introduction

Hudiy provides a set of environment variables to control specific functionalities. Using environment variables is necessary to apply configuration before file-based settings are loaded and core components are initialized. They are primarily used to configure Hudiy across different platforms prior to startup.

## Variables

### HUDIY_RENDERER

Specifies the type of renderer used. Possible values:  

- `direct` - Raspberry Pi only. Renderer for EGL mode (Raspberry Pi Zero 2, Raspberry Pi 3B, Raspberry Pi 3B+, Raspberry Pi 4).
- `composition` - Renderer for desktop mode (all Raspberry Pi variants and x86_64) and Raspberry Pi 5 EGL mode. (default)

### HUDIY_USE_AUTO_GL_SURFACE_FORMAT

Specifies the surface format negotiation method. Possible values:

- `0` - Forces RGBA mode. (default)
- `1` - Enables automatic negotiation.

### HUDIY_DISABLE_EQUALIZER

Controls the availability of the equalizer module. This variable overrides the `equalizer.enabled` config parameter. Possible values:

- `0` - Enables/disables the equalizer module based on the `equalizer.enabled` config parameter. (default)
- `1` - Disables equalizer module.

### HUDIY_LIMIT_HOTSPOT_BANDWIDTH

Controls bandwidth of the hotspot module. This variable overrides the `hotspot.bandwidth` config parameter. Possible values:

- `0` - Sets the hotspot bandwidth based on the `hotspot.bandwidth` config parameter. (default)
- `1` - Limits bandwidth to BG mode (2.4GHz).

### HUDIY_DISABLE_ANDROID_AUTO_DRM

Controls Android Auto DRM mode  usage. Overrides `androidAuto.useRpiDrm` and `androidAuto.useX86Drm` config parameters. Possible values:

- `0` - Sets the DRM mode based on the `androidAuto.useRpiDrm` and `androidAuto.useX86Drm` config parameters. (default)
- `1` - Disables DRM mode.
