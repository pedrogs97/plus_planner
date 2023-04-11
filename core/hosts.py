from django_hosts import host, patterns

host_patterns = patterns(
    "path.to",
    host(r"api", "api.urls", name="api"),
    host(r"beta", "beta.urls", name="beta"),
)
