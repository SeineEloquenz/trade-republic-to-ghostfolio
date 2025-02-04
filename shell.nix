with (import <nixpkgs> {});

mkShell {
  buildInputs = [ (python311.withPackages(ps: with ps; [ pandas])) ];
}
