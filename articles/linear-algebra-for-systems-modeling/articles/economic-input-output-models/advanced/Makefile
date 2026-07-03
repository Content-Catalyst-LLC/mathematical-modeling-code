.PHONY: smoke clean

smoke:
	@if command -v python3 >/dev/null 2>&1; then python3 python/advanced_input_output_review.py --output-dir outputs; else echo "python3 not found; skipping advanced layer."; fi

clean:
	rm -f outputs/reports/*.md outputs/tables/*.csv outputs/json/*.json
