.PHONY: run clean

run:
	c++ -O2 -std=c++17 policy_option_summary.cpp -o policy_option_summary
	./policy_option_summary > ../outputs/tables/cpp_policy_option_summary.csv 2> ../outputs/logs/cpp_policy_option_stderr.log

clean:
	rm -f policy_option_summary
