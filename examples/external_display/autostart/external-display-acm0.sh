http-server -p 12345 "$HOME/public/examples/external_display/widget" &

(
    while true; do
        "$HOME/.hudiy/share/web_viewer" --url "http://127.0.0.1:12345/dis.html" --device_descriptor /dev/ttyACM0 --rendering_mode 2 --width 320 --height 480
        
        EXIT_CODE=$?
        
        if [ "$EXIT_CODE" -eq 0 ]; then
            break
        else
            sleep 5
        fi
    done
) &