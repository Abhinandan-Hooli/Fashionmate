import json
from typing import Dict, List, Optional, Any
from google import genai
from google.genai import types

# Assuming products data is imported from a module
# from products_data import products
# For this example, I'll define a placeholder for products
products = []  # Replace with actual product data import

# --- Types for AI Response ---
class RecommendationIds:
    def __init__(self, data: Dict[str, Any]):
        self.top_id = data.get('top_id', '')
        self.bottom_id = data.get('bottom_id', '')
        self.footwear_id = data.get('footwear_id', '')
        self.accessory_id = data.get('accessory_id', '')
        self.style_tags = data.get('style_tags', [])
        self.color_palette = data.get('color_palette', [])
        self.reasoning = data.get('reasoning', '')
        self.occasion_title = data.get('occasion_title', '')

class FashionMateApp:
    def __init__(self):
        self.query = ''
        self.loading = False
        self.recommendation: Optional[RecommendationIds] = None
        self.error: Optional[str] = None
        
    def handle_style_me(self) -> None:
        """Handles the AI styling request"""
        if not self.query.strip():
            return
            
        self.loading = True
        self.error = None
        self.recommendation = None
        
        try:
            # Note: In Python, you should get API key from environment variable
            # api_key = os.environ.get('API_KEY')
            # For this conversion, I'm keeping the structure as in React
            ai = genai.Client(api_key='your_api_key_here')  # Replace with actual API key
            
            # Prepare the inventory context
            inventory_context = '\n'.join([
                f"ID: {p['ProductID']}, Name: {p['ProductName']}, Brand: {p['ProductBrand']}, "
                f"Color: {p['PrimaryColor']}, Desc: {p['Description']}"
                for p in products
            ])
            
            prompt = f"""
                You are FashionMate, an elite high-fashion AI stylist. 
                
                The user needs an outfit for: "{self.query}".
                
                Select the best matching items from the provided INVENTORY list below to create a complete, stylish outfit.
                You MUST pick exactly one 'top' (shirt/t-shirt/kurta/dress), one 'bottom' (jeans/trousers/skirt/shorts/leggings), one 'footwear', and one 'accessory' (watch/bag/jewellery/belt) from the inventory.
                If the user selects a dress or jumpsuit (which covers both top and bottom), set the 'bottom_id' to "NONE" or select a complementary legging if appropriate.
                
                INVENTORY:
                {inventory_context}

                Return a JSON object. Do not include markdown code blocks.
            """
            
            response = ai.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            'top_id': types.Schema(type=types.Type.STRING, description="ProductID of the selected top/dress"),
                            'bottom_id': types.Schema(type=types.Type.STRING, description="ProductID of the selected bottom (or 'NONE')"),
                            'footwear_id': types.Schema(type=types.Type.STRING, description="ProductID of the selected footwear"),
                            'accessory_id': types.Schema(type=types.Type.STRING, description="ProductID of the selected accessory"),
                            'style_tags': types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                            'color_palette': types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Hex codes or color names"),
                            'reasoning': types.Schema(type=types.Type.STRING, description="Why this outfit works for the occasion"),
                            'occasion_title': types.Schema(type=types.Type.STRING, description="A catchy title for this look")
                        }
                    )
                )
            )
            
            if response.text:
                data = json.loads(response.text)
                self.recommendation = RecommendationIds(data)
                
        except Exception as err:
            print(f"Error: {err}")
            self.error = "Our stylists are currently busy (AI Error). Please try again."
        finally:
            self.loading = False
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Helper to find product object by ID"""
        if product_id == 'NONE':
            return None
        for product in products:
            if str(product['ProductID']) == str(product_id):
                return product
        return None
    
    def render(self) -> str:
        """This would be the equivalent of the React render method"""
        # In a web framework, this would return HTML
        # For pure Python, we'll return a string representation
        if self.recommendation:
            return f"Recommendation: {self.recommendation.occasion_title}"
        return f"Query: {self.query}, Loading: {self.loading}"
    
    def set_query(self, query: str) -> None:
        """Equivalent to React's setState for query"""
        self.query = query

# --- ProductCard sub-component as a function ---
def render_product_card(product: Optional[Dict[str, Any]], category: str) -> str:
    """Renders a product card component"""
    if not product:
        return f"""
            <div class="h-full min-h-[150px] bg-slate-50 rounded-xl border-2 border-dashed border-slate-200 
                     flex items-center justify-center text-slate-400 flex-col gap-2 p-6 text-center">
                <div>No {category} selected</div>
            </div>
        """
    
    return f"""
        <div class="group bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl 
                    transition-all duration-300 border border-slate-100 flex flex-col h-full">
            <div class="p-6 flex flex-col flex-grow">
                <div class="text-xs font-bold text-rose-500 uppercase tracking-wide mb-2">
                    {category}
                </div>
                <div class="text-xs font-medium text-slate-500 mb-1">
                    {product['ProductBrand']}
                </div>
                <h3 class="font-serif text-lg leading-snug text-slate-900 mb-3">
                    {product['ProductName']}
                </h3>
                <p class="text-slate-600 text-sm line-clamp-3 mb-4">
                    {product['Description']}
                </p>
                <div class="mt-auto flex items-center justify-between pt-4 border-t border-slate-50">
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full border border-slate-200" 
                              style="background-color: {product['PrimaryColor']}"></span>
                        <span class="text-slate-500 text-sm">{product['PrimaryColor']}</span>
                    </div>
                    <span class="text-lg font-bold text-slate-900">₹{product['Price']}</span>
                </div>
            </div>
        </div>
    """

# Example usage
if __name__ == "__main__":
    app = FashionMateApp()
    app.set_query("A chic outfit for a summer garden party")
    app.handle_style_me()
    
    if app.recommendation:
        print(f"Occasion: {app.recommendation.occasion_title}")
        print(f"Reasoning: {app.recommendation.reasoning}")
        print(f"Style Tags: {', '.join(app.recommendation.style_tags)}")