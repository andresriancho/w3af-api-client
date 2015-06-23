FAST_TEST_PROFILE = """[profile]
description = sqli
name = sqli

[crawl.web_spider]
only_forward = True
follow_regex = .*
ignore_regex =

[audit.sqli]

[output.console]
verbose = True

[target]
target = http://127.0.0.1:8000/audit/sql_injection/

[misc-settings]
fuzz_cookies = False
fuzz_form_files = True
fuzz_url_filenames = False
fuzz_url_parts = False
fuzzed_files_extension = gif
fuzzable_headers =
form_fuzzing_mode = tmb
stop_on_first_exception = False
max_discovery_time = 120
interface = wlan1
local_ip_address = 10.1.2.24
non_targets =
msf_location = /opt/metasploit3/bin/

[http-settings]
timeout = 0
headers_file =
basic_auth_user =
basic_auth_passwd =
basic_auth_domain =
ntlm_auth_domain =
ntlm_auth_user =
ntlm_auth_passwd =
ntlm_auth_url =
cookie_jar_file =
ignore_session_cookies = False
proxy_port = 8080
proxy_address =
user_agent = w3af.org
rand_user_agent = False
max_file_size = 400000
max_http_retries = 2
max_requests_per_second = 0
always_404 =
never_404 =
string_match_404 =
url_parameter =

"""
