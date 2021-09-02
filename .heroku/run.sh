maturin build -m pyvtracer/Cargo.toml -i python3.9
find target -name vlib*p39*.whl -exec pip install {} \;
