{
  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        libraries = with pkgs;[
            libclang
            clang
            pkgs.stdenv.cc.cc.lib
            clangStdenv
            openssl
            glibc.dev
            gcc 
            mold
            boost188
            nlohmann_json
        ];

        packages = with pkgs; [
            pkg-config
            mold
            libclang
            clang
            clangStdenv
            pkgs.stdenv.cc.cc.lib
            openssl
            pkgs.cmake
            boost188
            sqlite
            nlohmann_json
        ];
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = packages;

          shellHook =
            ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath libraries}:$LD_LIBRARY_PATH
              export XDG_DATA_DIRS=${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS

              # if running from zsh, reenter zsh
              if [[ $(ps -e | grep $PPID) == *"zsh" ]]; then
                    export SHELL=zsh
                    zsh
                    exit
              fi
            '';
        };
      });
}
