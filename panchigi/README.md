# PanChigi friend invitation landing page

The public path is /panchigi/join/?code=<server UUID>. This isolated addition does not modify SheetCue files.
The site is static and has no analytics, tracking pixels, third-party fonts, API calls, or automatic store redirect.
The query is validated before a single custom-scheme attempt. The page offers a manual app-open action and code copy.
An app install does not preserve the invite; revisit this link or paste the code afterwards.

## Stores and associations

- Android package: com.panchigi (client ProjectSettings). Public Play lookup returned 404 on 2026-10-23.
- iOS team and bundle: XF5CMG6QGW.com.panchigi (client ProjectSettings). Apple KR lookup returned resultCount 0.
- Both store buttons deliberately say 곧 출시돼요. No App Store numeric ID was invented.
- assetlinks.json currently contains the locally read Windows debug signing certificate only.
- TODO BEFORE PUBLICATION: add the Play App Signing SHA-256 from Play Console > App integrity/App signing;
  local upload/debug keys do not establish trust for Play-installed apps. An upload certificate was not available locally.
- The iOS App ID and signed provisioning profile must enable Associated Domains. After publication check the HTTPS AASA
  response (no redirect, correct JSON/MIME), Apple CDN ingestion, signed entitlements, and cold/warm activation on a device.
- .nojekyll permits .well-known publication. Existing site content and association entries must be preserved in future changes.

## Social previews

HTML contains server-visible OG and Twitter tags; JavaScript does not construct them. og:url/canonical never include
an invite code. Different query URLs receive identical generic metadata, so no account or room details appear in a crawler card.
The 1200x630 PNG is the primary OG/Twitter image; a 600x600 alternative is also declared for square-cropping consumers.
Each image is below 300 KB. A messenger chooses which image to display; platform rendering is not controlled by this page.
All illustrations are existing approved Image Gen exports. art-provenance.json binds their client paths, hashes, generated
sources and prompts. Rebuild with Pillow: python panchigi/build-preview-art.py <client-root>.

References checked 2026-10-23:
- Kakao official staff guidance: https://devtalk.kakao.com/t/topic/140526 (URL previews are 2:1; smart crop is platform-controlled).
  The primary 1200x630 artwork keeps content inside the central 1200x600 safe area; the square alternative is additional, not a promise that Kakao selects it.
- Kakao scraper / OG mapping: https://developers.kakao.com/docs/ko/message-template/common
- Kakao cache-clear/debugger (login required): https://developers.kakao.com/tool/debugger/sharing
  Legacy cache-clear entry: https://developers.kakao.com/tool/clear/og
- Meta sharing image rules: https://developers.facebook.com/docs/sharing/webmasters/images/
  (automated retrieval returned 429; do not claim a live Facebook debugger pass).
- X large card rules: https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image
- Facebook cache refresh after publication: https://developers.facebook.com/tools/debug/

Use validate-page.py for static metadata, image, association and unrelated-file checks. Local desktop/mobile renders and
Kakao-style/iMessage-style mock cards are review evidence only. The site is intentionally not published until coordinator
approval. Actual Kakao, LINE, iMessage, Discord, Slack, Telegram, X and Messenger unfurls must be checked on the published
URL after approval; crawler caching, image selection and device handling cannot be proved with a local render.
