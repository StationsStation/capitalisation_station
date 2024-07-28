#! /usr/bin/fish

while true
    poetry run adev -v -n 4 fmt -co && poetry run adev -n 4 lint -co && poetry run adev -n 4 test && echo done
end


