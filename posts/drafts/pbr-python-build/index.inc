https://docs.openstack.org/pbr/latest/user/features.html

That feature is cool:

    We then walk Git history back to the last release. Within each commit
    we look for a Sem-Ver: pseudo header and, if found, parse it looking
    for keywords. Unknown symbols are not an error (so that folk can’t
    wedge pbr or break their tree), but we will emit an info-level warning
    message. The following symbols are recognized:

        feature
        api-break
        deprecation
        bugfix
