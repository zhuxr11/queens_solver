// --- Custom URL adjustment script ---
async function test_url_exist(url) {
  try {
    let response = await fetch(url, { method: "HEAD" });

    // Some servers don't support HEAD, so retry with GET if needed
    if (!response.ok && response.status === 405) {
      response = await fetch(url, { method: "GET" });
    }

    if (response.ok) {
      // If there is anchor, implement additional check on anchor
      const [base_url, anchor] = url.split("#");
      if (anchor) {
        // Load target base URL and check for anchor
        const html_text = await fetch(base_url).then(res => res.text());
        const parser = new DOMParser();
        const loaded_doc = parser.parseFromString(html_text, "text/html");
        const element = loaded_doc.getElementById(anchor);
        if (!element) {
            return `error: Anchor not found: #${anchor} in ${base_url}`;
        }
      }
      return url; // URL exists
    } else {
      return `error: URL not found (status ${response.status}): ${url}`;
    }
  } catch (err) {
    return `error: Failed to reach URL: ${url}\n${err}`;
  }
}

dynamic_version_links = async function () {
    const current_version_span = document.querySelector('.rst-current-version');
    const current_version = current_version_span
        ? current_version_span.textContent.match(/Current:\s*(\S+)/)[1]
        : 'master';

    // Get base URL before /${currentVersion}/ for fallback URL construction
    const regex = new RegExp(`/${current_version}/`);
    const version_segment = `/${current_version}/`;
    const index = window.location.href.indexOf(version_segment);
    const base_url = window.location.href.substring(0, index);

    const links = document.querySelectorAll('.rst-other-versions a');
    links.forEach(async link => {
        const branch = link.textContent.trim();
        if (branch) {
            const new_url = window.location.href.replace(regex, `/${branch}/`);
            const new_url_test = await test_url_exist(new_url);
            if (!new_url_test.startsWith("error: ")) {
                link.href = new_url;
            } else {
                const fallback = `${base_url}/${branch}/index.html`;
                if (new_url.includes("#")) {
                    const new_url_no_anchor = new_url.split("#")[0];
                    const new_url_no_anchor_test = test_url_exist(new_url_no_anchor)
                    if (!new_url_no_anchor_test.startsWith("error: ")) {
                        link.href = await test_url_exist(new_url_no_anchor);
                    } else {
                        link.href = fallback;
                    }
                } else {
                    link.href = fallback;
                }
            }
        }
    });

    const dev_message_link = document.querySelector('p > strong > a');
    // Resolve relative href to absolute URL
    const dev_message_abs_link = new URL(dev_message_link.getAttribute("href"), window.location.href);
    const latest_release_branch = dev_message_abs_link.pathname.split("/")[1];
    if (dev_message_link) {
        const current_url_no_anchor = window.location.href.split('#')[0];
        const new_url = current_url_no_anchor.replace(regex, `/${latest_release_branch}/`);
        const new_url_test = await test_url_exist(new_url);
        if (!new_url_test.startsWith("error: ")) {
            dev_message_link.href = new_url;
        } else {
            dev_message_link.href = `${base_url}/${latest_release_branch}/index.html`;
        }
    }
}

document.addEventListener("DOMContentLoaded", dynamic_version_links);
window.onhashchange = dynamic_version_links;
