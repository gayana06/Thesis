echo "Copy config.py"
./apply_oracle_py.sh
echo "Copy proxy-server.cong"
./apply-proxy-config.sh
echo "Recompile proxies"
./recompile-proxies.sh
echo "Clean"
rm config.py
rm proxy-server.conf
echo "Proxies all done"
