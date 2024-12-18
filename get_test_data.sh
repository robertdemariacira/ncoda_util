cd "$(dirname "$0")"

pushd tests/manual/in_data/example/
wget https://irma.cira.colostate.edu/index.php/s/23RgTs7JX5ByybW/download/ncoda_ocean_example.zip
unzip ncoda_ocean_example.zip
rm ncoda_ocean_example.zip
popd

pushd tests/manual/in_data/static/
wget https://irma.cira.colostate.edu/index.php/s/tH5GDFdK9sZHErH/download/ncoda_static_data.zip
unzip ncoda_static_data.zip
rm ncoda_static_data.zip
popd