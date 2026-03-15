# Building Guide

This guide will help you build the project on your local machine. The process will require you to provide a ROM of the US version of the game.

These steps cover: Running the recompiler and building the project.

## 1. Clone the MarioKart64Recomp Repository
This project makes use of submodules so you will need to clone the repository with the `--recurse-submodules` flag.

```bash
git clone --recurse-submodules
# if you forgot to clone with --recurse-submodules
# cd /path/to/cloned/repo && git submodule update --init --recursive
```

## 2. Install Dependencies

### Linux
For Linux the instructions for Ubuntu are provided, but you can find the equivalent packages for your preferred distro.

```bash
# For Ubuntu, simply run:
sudo apt-get install cmake ninja-build libsdl2-dev libgtk-3-dev lld llvm clang
```

### Windows
You will need to install [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/).
In the setup process you'll need to select the following options and tools for installation:
- Desktop development with C++
- C++ Clang Compiler for Windows
- C++ CMake tools for Windows

The other tool necessary will be `make` which can be installe via [Chocolatey](https://chocolatey.org/):
```bash
choco install make
```

## 3. Generating the C code
Copy the ROM to the root of the MarioKart64Recomp repository with this filename:

- `mk64.us.z64`

Now that you have the required files, you must build [N64Recomp](https://github.com/Mr-Wiseguy/N64Recomp) and run it to generate the C code to be compiled. The building instructions can be found [here](https://github.com/Mr-Wiseguy/N64Recomp?tab=readme-ov-file#building). That will build the executables: `N64Recomp` and `RSPRecomp` which you should copy to the root of the MarioKart64Recomp repository.

After that, go back to the repository root, and run the following commands:
```bash
./N64Recomp us.toml
./RSPRecomp aspMain.us.toml
```

## 4. Building the Project

Finally, you can build the project! :rocket:

On Windows, you can open the repository folder with Visual Studio, and you'll be able to `[build / run / debug]` the project from there.

If you prefer the command line or you're on a Unix platform you can build the project using CMake:

```bash
cmake -S . -B build-cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -G Ninja -DCMAKE_BUILD_TYPE=Release # or Debug if you want to debug
cmake --build build-cmake --target MarioKart64Recompiled -j$(nproc) --config Release # or Debug
```

## 5. Success

Voilà! You should now have a `MarioKart64Recompiled` executable in the build directory! If you used Visual Studio this will be `out/build/x64-[Configuration]` and if you used the provided CMake commands then this will be `build-cmake`. You will need to run the executable out of the root folder of this project or copy the assets folder to the build folder to run it.

---

## Building for WebAssembly (WASM) — Experimental

> **Status:** Early / in-progress port.  The infrastructure is in place but a
> fully functional WebGL rendering back-end is not yet implemented.

### Prerequisites

1. Install and activate the **Emscripten SDK** (emsdk):

   ```bash
   git clone https://github.com/emscripten-core/emsdk.git
   cd emsdk
   ./emsdk install latest
   ./emsdk activate latest
   source ./emsdk_env.sh   # re-run this in each new shell
   ```

2. Complete steps 1–3 above (clone, install dependencies, generate C code).

3. Make sure `cmake` and `ninja` are available on `$PATH`.

### Building

Run the provided helper script from the repository root:

```bash
./build_wasm.sh Release   # or Debug
```

This is equivalent to:

```bash
emcmake cmake -S . -B build-wasm -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build-wasm --target MarioKart64Recompiled -j$(nproc)
```

The linker will produce three files inside `build-wasm/`:

| File | Description |
|------|-------------|
| `MarioKart64Recompiled.html` | Host page with the ROM picker and canvas |
| `MarioKart64Recompiled.js`  | Emscripten JS loader / glue code |
| `MarioKart64Recompiled.wasm`| Compiled WebAssembly module |

### Running

Because of browser security restrictions, the files must be served over HTTP
(not opened from the filesystem directly):

```bash
cd build-wasm
python3 -m http.server 8080
```

Then open <http://localhost:8080/MarioKart64Recompiled.html> in a modern
browser (Chrome / Firefox / Edge with SharedArrayBuffer enabled).

### Notes

* **ROM upload:** the page includes a file picker so you can provide your own
  copy of the **US release** of Mario Kart 64 at runtime — no server-side ROM
  storage is involved.  Only the US (NTSC) version is supported; other regional
  releases will be rejected by the game loader.
* **SharedArrayBuffer** must be enabled in the browser for multi-threaded
  operation.  When serving locally with Python the necessary COOP/COEP headers
  are not set by default; use a small server wrapper or browser flags for
  testing.
* The native graphics back-end (RT64) uses Vulkan / DirectX 12 / Metal which
  are not available in browsers.  Porting the renderer to WebGL / WebGPU is the
  main remaining work item.

