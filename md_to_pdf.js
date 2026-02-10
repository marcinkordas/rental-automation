const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const { marked } = require("marked");

async function convertMarkdownToPDF(mdFilePath) {
  try {
    // Read Markdown file
    const markdown = fs.readFileSync(mdFilePath, "utf-8");

    // Convert to HTML
    const htmlContent = marked.parse(markdown);

    // Create styled HTML document
    const styledHTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
        }
        
        h1 {
            font-size: 18pt;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
            page-break-after: avoid;
            page-break-inside: avoid;
        }
        
        h2 {
            font-size: 14pt;
            margin-top: 25px;
            margin-bottom: 15px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
            page-break-after: avoid;
            page-break-inside: avoid;
        }
        
        h3 {
            font-size: 12pt;
            margin-top: 20px;
            margin-bottom: 10px;
            page-break-after: avoid;
            page-break-inside: avoid;
        }
        
        p {
            margin-bottom: 8px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            page-break-inside: avoid;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
        
        hr {
            border: none;
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }
        
        strong {
            font-weight: 600;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        /* Prevent page breaks after section labels */
        .section-label {
            page-break-after: avoid;
        }
    </style>
    <script>
        // Mark paragraphs that are section labels (Polski:, English:, Zabrania się:, etc.)
        window.addEventListener('DOMContentLoaded', function() {
            const paragraphs = document.querySelectorAll('p');
            paragraphs.forEach(p => {
                const text = p.textContent.trim();
                const strongOnly = p.children.length === 1 && p.children[0].tagName === 'STRONG';
                if (strongOnly && text.endsWith(':')) {
                    p.classList.add('section-label');
                }
            });
        });
    </script>
</head>
<body>
    ${htmlContent}
</body>
</html>
        `;

    // Launch headless browser
    const browser = await puppeteer.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });

    const page = await browser.newPage();

    // Set content and generate PDF
    await page.setContent(styledHTML, { waitUntil: "networkidle0" });

    const pdfPath = mdFilePath.replace(".md", ".pdf");
    await page.pdf({
      path: pdfPath,
      format: "A4",
      margin: {
        top: "20mm",
        right: "20mm",
        bottom: "25mm",
        left: "20mm",
      },
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '\u003cdiv style="font-size: 1px;">\u003c/div\u003e',
      footerTemplate: `
        \u003cdiv style="width: 100%; font-size: 9pt; text-align: center; color: #666; padding-top: 5mm;"\u003e
          Strona \u003cspan class="pageNumber"\u003e\u003c/span\u003e / \u003cspan class="totalPages"\u003e\u003c/span\u003e
        \u003c/div\u003e
      `,
    });

    await browser.close();

    console.log(`✅ PDF created: ${pdfPath}`);
    return pdfPath;
  } catch (error) {
    console.error(`❌ Error converting ${mdFilePath}:`, error.message);
    process.exit(1);
  }
}

// Main execution
if (process.argv.length < 3) {
  console.error("Usage: node md_to_pdf.js <markdown-file-path>");
  process.exit(1);
}

const mdFile = process.argv[2];
if (!fs.existsSync(mdFile)) {
  console.error(`File not found: ${mdFile}`);
  process.exit(1);
}

convertMarkdownToPDF(mdFile);
