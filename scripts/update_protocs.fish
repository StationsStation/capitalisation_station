

for protocol in ( ls packages/eightballer/protocols/)
    echo doing $protocol
    export PROTO_PATH=packages/eightballer/protocols/$protocol
    export PYTHON_OUT=build/gen
    protoc --proto_path=$PROTO_PATH --python_out=$PYTHON_OUT  packages/eightballer/protocols/$protocol/$protocol.proto
     mv build/gen/(echo $protocol)_pb2.py packages/eightballer/protocols/$protocol/
end
