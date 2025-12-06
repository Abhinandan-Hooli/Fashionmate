<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FashionMate - AI Personal Styling Engine</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        :root {
            --rose-500: #f43f5e;
            --rose-200: #fecdd3;
            --rose-100: #ffe4e6;
            --rose-600: #e11d48;
            --rose-900: #881337;
            --slate-50: #f8fafc;
            --slate-100: #f1f5f9;
            --slate-200: #e2e8f0;
            --slate-300: #cbd5e1;
            --slate-400: #94a3b8;
            --slate-500: #64748b;
            --slate-600: #475569;
            --slate-800: #1e293b;
            --slate-900: #0f172a;
            --teal-200: #99f6e4;
            --amber-500: #f59e0b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: var(--slate-50);
            color: var(--slate-800);
            min-height: 100vh;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        .selection\:bg-rose-200 ::selection {
            background-color: var(--rose-200);
            color: var(--rose-900);
        }

        header {
            position: sticky;
            top: 0;
            z-index: 50;
            border-bottom: 1px solid rgba(255, 255, 255, 0.4);
        }

        main {
            max-width: 72rem;
            margin: 0 auto;
            padding: 3rem 1.5rem;
        }

        .font-serif {
            font-family: Georgia, 'Times New Roman', Times, serif;
        }

        .rounded-xl {
            border-radius: 1rem;
        }

        .rounded-lg {
            border-radius: 0.5rem;
        }

        .shadow-xl {
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        .shadow-lg {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        .shadow-sm {
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        .line-clamp-3 {
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .animate-spin {
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .animate-fade-in-up {
            animation: fadeInUp 0.5s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Grid System */
        .grid {
            display: grid;
            gap: 1.5rem;
        }

        .grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
        .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

        @media (min-width: 768px) {
            .md\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
        }

        @media (min-width: 1024px) {
            .lg\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
            .lg\:grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
            .lg\:col-span-2 { grid-column: span 2 / span 2; }
        }

        /* Utility Classes */
        .flex { display: flex; }
        .flex-col { flex-direction: column; }
        .items-center { align-items: center; }
        .justify-center { justify-content: center; }
        .justify-between { justify-content: space-between; }
        .flex-wrap { flex-wrap: wrap; }
        .gap-1 { gap: 0.25rem; }
        .gap-2 { gap: 0.5rem; }
        .gap-3 { gap: 0.75rem; }
        .gap-4 { gap: 1rem; }
        .gap-6 { gap: 1.5rem; }
        .gap-8 { gap: 2rem; }
        .space-y-2 > * + * { margin-top: 0.5rem; }
        .space-y-4 > * + * { margin-top: 1rem; }
        .space-y-8 > * + * { margin-top: 2rem; }
        .space-y-12 > * + * { margin-top: 3rem; }

        .w-5 { width: 1.25rem; }
        .h-5 { height: 1.25rem; }
        .w-6 { width: 1.5rem; }
        .h-6 { height: 1.5rem; }
        .w-16 { width: 4rem; }
        .h-16 { height: 4rem; }

        .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
        .px-4 { padding-left: 1rem; padding-right: 1rem; }
        .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
        .px-8 { padding-left: 2rem; padding-right: 2rem; }
        .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
        .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
        .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
        .py-4 { padding-top: 1rem; padding-bottom: 1rem; }
        .py-8 { padding-top: 2rem; padding-bottom: 2rem; }
        .py-12 { padding-top: 3rem; padding-bottom: 3rem; }

        .mt-2 { margin-top: 0.5rem; }
        .mt-4 { margin-top: 1rem; }
        .mt-20 { margin-top: 5rem; }
        .mb-2 { margin-bottom: 0.5rem; }
        .mb-4 { margin-bottom: 1rem; }
        .mb-20 { margin-bottom: 5rem; }

        .text-center { text-align: center; }
        .text-lg { font-size: 1.125rem; line-height: 1.75rem; }
        .text-xl { font-size: 1.25rem; line-height: 1.75rem; }
        .text-2xl { font-size: 1.5rem; line-height: 2rem; }
        .text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
        .text-5xl { font-size: 3rem; line-height: 1; }
        .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
        .text-xs { font-size: 0.75rem; line-height: 1rem; }

        .font-bold { font-weight: 700; }
        .font-medium { font-weight: 500; }
        .font-serif { font-family: Georgia, serif; }

        .tracking-wide { letter-spacing: 0.025em; }
        .tracking-wider { letter-spacing: 0.05em; }

        .uppercase { text-transform: uppercase; }
        .italic { font-style: italic; }

        .relative { position: relative; }
        .absolute { position: absolute; }
        .sticky { position: sticky; }

        .border { border-width: 1px; }
        .border-2 { border-width: 2px; }
        .border-dashed { border-style: dashed; }
        .border-t { border-top-width: 1px; }

        .rounded-full { border-radius: 9999px; }

        .opacity-50 { opacity: 0.5; }
        .opacity-25 { opacity: 0.25; }

        .transition-all { transition-property: all; }
        .transition-opacity { transition-property: opacity; }
        .transition-colors { transition-property: background-color, border-color, color; }
        .duration-300 { transition-duration: 300ms; }

        .hover\:shadow-xl:hover { box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); }
        .hover\:bg-slate-800:hover { background-color: var(--slate-800); }

        .group:hover .group-hover\:opacity-50 { opacity: 0.5; }
        .group:hover .group-hover\:opacity-100 { opacity: 1; }

        .disabled\:opacity-50:disabled { opacity: 0.5; }
        .disabled\:cursor-not-allowed:disabled { cursor: not-allowed; }

        /* Custom Components */
        .product-card {
            background: white;
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--slate-100);
            display: flex;
            flex-direction: column;
            height: 100%;
            transition: all 0.3s;
        }

        .product-card:hover {
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        .product-card-content {
            padding: 1.5rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .input-group {
            position: relative;
        }

        .input-glow {
            position: absolute;
            inset: -0.25rem;
            background: linear-gradient(to right, var(--rose-200), var(--teal-200));
            border-radius: 1rem;
            filter: blur(4px);
            opacity: 0.25;
            transition: opacity 1s;
        }

        .input-glow:hover {
            opacity: 0.5;
            transition-duration: 200ms;
        }

        .input-container {
            position: relative;
            display: flex;
            align-items: center;
            background: white;
            border-radius: 1rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--slate-100);
            padding: 0.5rem;
        }

        input {
            width: 100%;
            padding: 1rem;
            background: transparent;
            border: none;
            font-size: 1.125rem;
            color: var(--slate-800);
        }

        input:focus {
            outline: none;
            box-shadow: none;
        }

        input::placeholder {
            color: var(--slate-300);
        }

        button {
            background-color: var(--slate-900);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            font-weight: 500;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        button:hover {
            background-color: var(--slate-800);
        }

        .tag {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.25rem 0.75rem;
            background: white;
            border: 1px solid var(--slate-200);
            border-radius: 9999px;
            font-size: 0.875rem;
            color: var(--slate-600);
        }

        .color-circle {
            width: 4rem;
            height: 4rem;
            border-radius: 9999px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 2px solid var(--slate-50);
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <header class="glass-panel" style="border-bottom: 1px solid rgba(255, 255, 255, 0.4);">
        <div style="max-width: 72rem; margin: 0 auto; padding: 0 1.5rem; height: 5rem; display: flex; align-items: center; justify-content: space-between;">
            <div class="flex items-center gap-2">
                <i class="fas fa-sparkles" style="color: var(--rose-500); font-size: 1.5rem;"></i>
                <h1 class="font-serif font-bold" style="font-size: 1.5rem; color: var(--slate-900);">
                    FashionMate<span style="color: var(--rose-500);">.</span>
                </h1>
            </div>
            <div class="font-medium" style="color: var(--slate-500); font-size: 0.875rem; display: none;">
                AI Personal Styling Engine
            </div>
        </div>
    </header>

    <main>
        <section class="text-center space-y-8" style="max-width: 48rem; margin: 0 auto 5rem;">
            <h2 class="font-serif" style="font-size: 3rem; line-height: 1.25; color: var(--slate-900);">
                What are you dressing for today?
            </h2>
            <p style="font-size: 1.125rem; color: var(--slate-600); line-height: 1.75;">
                From casual brunches to evening galas, describe your occasion and let our AI 
                curate the perfect look from our exclusive collection.
            </p>

            <div class="input-group">
                <div class="input-glow"></div>
                <div class="input-container">
                    <div style="padding-left: 1rem; color: var(--slate-400);">
                        <i class="fas fa-user" style="font-size: 1.25rem;"></i>
                    </div>
                    <input 
                        type="text"
                        id="queryInput"
                        placeholder="e.g., A chic outfit for a summer garden party..."
                        style="padding: 1rem;"
                    />
                    <button id="styleButton" onclick="handleStyleMe()">
                        <span id="buttonText">Style Me</span>
                        <i class="fas fa-arrow-right" id="buttonIcon" style="font-size: 1rem;"></i>
                    </button>
                </div>
            </div>
            
            <div id="error" style="display: none; color: #ef4444; background-color: #fef2f2; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;"></div>
        </section>

        <div id="results" class="animate-fade-in-up" style="display: none;">
            <div class="text-center space-y-4">
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background-color: var(--rose-100); color: var(--rose-600); border-radius: 9999px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em;">
                    Your Curated Look
                </span>
                <h3 id="occasionTitle" class="font-serif" style="font-size: 2.25rem;"></h3>
                <div id="styleTags" class="flex justify-center flex-wrap gap-2" style="margin-top: 1rem;"></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" style="margin-top: 3rem;">
                <div id="topCard"></div>
                <div id="bottomCard"></div>
                <div id="footwearCard"></div>
                <div id="accessoryCard"></div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8" style="margin-top: 3rem;">
                <div class="lg:col-span-2" style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); border: 1px solid var(--slate-100);">
                    <h4 class="font-serif" style="font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                        <i class="fas fa-sparkles" style="color: var(--amber-500); font-size: 1.25rem;"></i> Stylist's Note
                    </h4>
                    <p id="reasoning" style="color: var(--slate-600); font-size: 1.125rem; line-height: 1.75; font-style: italic;"></p>
                </div>
                
                <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); border: 1px solid var(--slate-100); display: flex; flex-direction: column; justify-content: center;">
                    <h4 style="font-size: 0.875rem; font-weight: bold; text-transform: uppercase; color: var(--slate-400); letter-spacing: 0.05em; margin-bottom: 1rem;">
                        Color Palette
                    </h4>
                    <div id="colorPalette" class="flex gap-4"></div>
                </div>
            </div>
        </div>
    </main>
    
    <footer style="background: white; border-top: 1px solid var(--slate-100); padding: 3rem 0; margin-top: 5rem;">
        <div style="max-width: 72rem; margin: 0 auto; padding: 0 1.5rem; text-align: center; color: var(--slate-400);">
            <p class="font-serif" style="font-size: 1.125rem; color: var(--slate-900); margin-bottom: 0.5rem;">FashionMate.</p>
            <p>Powered by Google Gemini • Fashion dataset included</p>
        </div>
    </footer>

    <script>
        async function handleStyleMe() {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) return;
            
            const button = document.getElementById('styleButton');
            const buttonText = document.getElementById('buttonText');
            const buttonIcon = document.getElementById('buttonIcon');
            const errorDiv = document.getElementById('error');
            
            button.disabled = true;
            buttonText.textContent = 'Styling...';
            buttonIcon.className = 'fas fa-spinner fa-spin';
            errorDiv.style.display = 'none';
            
            try {
                const response = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Something went wrong');
                }
                
                displayResults(data);
                
                document.getElementById('results').style.display = 'block';
                document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
                
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            } finally {
                button.disabled = false;
                buttonText.textContent = 'Style Me';
                buttonIcon.className = 'fas fa-arrow-right';
            }
        }

        function displayResults(recommendation) {
            document.getElementById('occasionTitle').textContent = recommendation.occasion_title;
            document.getElementById('reasoning').textContent = `"${recommendation.reasoning}"`;
            
            // Display style tags
            const tagsContainer = document.getElementById('styleTags');
            tagsContainer.innerHTML = '';
            recommendation.style_tags.forEach(tag => {
                const tagElement = document.createElement('span');
                tagElement.className = 'tag';
                tagElement.innerHTML = `<i class="fas fa-tag" style="font-size: 0.75rem;"></i> ${tag}`;
                tagsContainer.appendChild(tagElement);
            });
            
            // Display product cards
            displayProductCard('topCard', 'Top', recommendation.top_id);
            displayProductCard('bottomCard', 'Bottom', recommendation.bottom_id);
            displayProductCard('footwearCard', 'Footwear', recommendation.footwear_id);
            displayProductCard('accessoryCard', 'Accessory', recommendation.accessory_id);
            
            // Display color palette
            const paletteContainer = document.getElementById('colorPalette');
            paletteContainer.innerHTML = '';
            recommendation.color_palette.forEach(color => {
                const colorElement = document.createElement('div');
                colorElement.className = 'relative group';
                colorElement.innerHTML = `
                    <div class="color-circle" style="background-color: ${color.toLowerCase().includes('gold') ? '#FFD700' : color}"></div>
                    <span style="position: absolute; top: 100%; left: 50%; transform: translateX(-50%); margin-top: 0.5rem; font-size: 0.75rem; font-weight: 500; color: var(--slate-500); opacity: 0; transition: opacity 0.2s;">
                        ${color}
                    </span>
                `;
                colorElement.addEventListener('mouseenter', () => {
                    colorElement.querySelector('span').style.opacity = '1';
                });
                colorElement.addEventListener('mouseleave', () => {
                    colorElement.querySelector('span').style.opacity = '0';
                });
                paletteContainer.appendChild(colorElement);
            });
        }

        async function displayProductCard(containerId, category, productId) {
            const container = document.getElementById(containerId);
            
            if (productId === 'NONE' || !productId) {
                container.innerHTML = `
                    <div style="height: 100%; min-height: 150px; background-color: var(--slate-50); border-radius: 1rem; border: 2px dashed var(--slate-200); display: flex; align-items: center; justify-content: center; color: var(--slate-400); flex-direction: column; gap: 0.5rem; padding: 1.5rem; text-align: center;">
                        <i class="fas fa-shopping-bag" style="font-size: 1.5rem; opacity: 0.5;"></i>
                        <span style="font-size: 0.875rem; font-weight: 500;">No ${category} selected</span>
                    </div>
                `;
                return;
            }
            
            try {
                const response = await fetch('/api/products');
                const products = await response.json();
                const product = products.find(p => String(p.ProductID) === String(productId));
                
                if (product) {
                    container.innerHTML = `
                        <div class="product-card">
                            <div class="product-card-content">
                                <div style="font-size: 0.75rem; font-weight: bold; color: var(--rose-500); text-transform: uppercase; letter-spacing: 0.025em; margin-bottom: 0.5rem;">
                                    ${category}
                                </div>
                                <div style="font-size: 0.75rem; font-weight: 500; color: var(--slate-500); margin-bottom: 0.25rem;">
                                    ${product.ProductBrand}
                                </div>
                                <h3 class="font-serif" style="font-size: 1.125rem; line-height: 1.375; color: var(--slate-900); margin-bottom: 0.75rem;">
                                    ${product.ProductName}
                                </h3>
                                <p style="color: var(--slate-600); font-size: 0.875rem; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 1rem;">
                                    ${product.Description}
                                </p>
                                <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid var(--slate-50);">
                                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                                        <span style="width: 0.75rem; height: 0.75rem; border-radius: 9999px; border: 1px solid var(--slate-200); background-color: ${product.PrimaryColor};"></span>
                                        <span style="color: var(--slate-500); font-size: 0.875rem;">${product.PrimaryColor}</span>
                                    </div>
                                    <span style="font-size: 1.125rem; font-weight: bold; color: var(--slate-900);">₹${product.Price}</span>
                                </div>
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error fetching product:', error);
            }
        }

        document.getElementById('queryInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                handleStyleMe();
            }
        });
    </script>
</body>
</html>