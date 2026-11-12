# Watts Course Policies

This repository publishes the shared Watts College course policies linked from Canvas courses.

**Live page:** https://watts-college.github.io/watts-course-policies/

## Where to make changes

| What you want to update | File |
| --- | --- |
| Policy wording, Resources, headings, or the table of contents | `index.md` |
| Colors, spacing, mobile layout, or print styling | `assets/css/policies.css` |
| Page structure, logo placement, or logo alternative text | `_layouts/policies.html` |
| College logo | `assets/posts/ASU_WattsPublicService_3_Horiz_RGB_Black_600ppi.png` |
| Browser tab icon | `assets/icons/favicon-32x32.png` |
| Site address or Markdown settings | `_config.yml` |
| Redirect from the older policies page | `review.html` |

The Resources section is part of `index.md`; there is no separate resources page. The table of contents lists the main sections only. UCENT 150 is a subsection of Resources.

## Making and publishing an update

1. Create a branch and edit the relevant file.
2. Open a pull request. The **Validate policies site** check builds the site and checks local links, section anchors, retained assets, and the older-page redirect.
3. Review the changes. For visual changes, also check desktop/mobile layout, keyboard navigation, and zoom; passing the build does not establish accessibility conformance.
4. Merge the approved pull request into `main`. The existing GitHub-managed **pages build and deployment** workflow publishes the site.
5. Confirm deployment succeeded and review the live page. Refresh the browser if it still displays an older version.

The validation workflow does not deploy the site or change GitHub Pages settings. If a deployment times out after a successful build, inspect the deployment logs before retrying; a cancelled deployment may require a fresh publishing attempt.

## Local preview

With Ruby and Bundler installed:

```sh
bundle install
bundle exec jekyll serve
```

Open http://localhost:4000/watts-course-policies/ in a browser. To build and check the output instead:

```sh
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/validate_site.py _site
```

## Important conventions

- Keep the page's white background, dark text, and underlined ASU Maroon (`#8C1D40`) links.
- Keep a single main heading and nest subsections logically.
- Preserve existing heading anchors when possible because Canvas courses or other sites may link directly to them.
- Keep the logo and favicon at their current paths unless all references are updated.
- `/review/` redirects to the current policies page; its script preserves query strings and section fragments, with a refresh/link fallback when scripts are unavailable.
- The existing analytics setting and include are retained. The tracking ID's ownership and continued suitability have not been confirmed.

## Repository cleanup

The copied course lessons, datasets, schedules, blog posts, old theme, and JavaScript tooling were removed from the current file tree. The former `/review/` policies address is retained as a redirect. Other removed course-page and download addresses are not retained; external links to those materials may stop working after the cleanup is published.

Git history retains the removed files. To reverse the cleanup, revert its commit or pull request rather than rewriting history.

