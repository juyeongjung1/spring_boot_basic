package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;

@Controller
@RequestMapping("/product")

public class ProductController {
	//ここに、ProductRepositoryを依存性の注入してください。

	
	@GetMapping("/findAll")
	public String showProductList(Model model) {
		//findAllメソッドを呼び出して、List<Product> listの変数に代入してください。
		
		//Modelに、listを設定してください。キー名はproducts
		
		return "product/list";
	}
	
	
	@GetMapping("/")
	public String showSearchView() {
		return "product/search";
	}
	
	@GetMapping("/findById")
	public String showProductById(int id, Model model) {
		//findByIdメソッドを実行し、Product型の変数productに代入してください。
		
		//Modelに、productを設定してください。キー名はproduct
		
		return "product/detail";
	}
	
	@GetMapping("/findByPrice")
	public String showProductListByPrice(int price, Model model) {
		//findByPriceメソッドを実行し、List<Product> listの変数に代入してください。
		
		//model.addAttribute("products", list);
		return "product/list";
	}
	
	@GetMapping("/findByNameAndPrice")
	public String showProductListByNameAndPrice(String name, int price, Model model) {
		//findByNameAndPriceメソッドを実行し、List<Product> listの変数に代入してください。
		
		//model.addAttribute("products", list);
		return "product/list";
	}
	
	@GetMapping("/insert")
	public String showProductInsertView() {
		return "product/insert";
	}
	
	@PostMapping("/insert")
	public String insertProduct(ProductForm productForm, Model model) {
		Product product = new Product();
		//productエンティティのnameとpriceに、productFormのNameとPriceをセットしてください。
		
		//saveメソッドを実行し、Product型の変数productに代入してください。
		
		model.addAttribute("product", product);
		return ""; // 「product/result」を表示してください。
	}
	
	@GetMapping("update/{id}")
	                    //URLからのidを取得できるアノテーションを付けてください
	public String showUpdateInputView(int id, Model model) {
		
		//主キー検索をしてください。
		
		//model.addAttribute("product", product);
		return "product/update_input";
	}

	@PostMapping("/update")
	public String updateProduct(ProductForm productForm, Model model) {
		Product product = new Product();
		//productエンティティのnameとpriceに、productFormのNameとPriceをセットしてください。
		
		//saveメソッドを実行し、Product型の変数productに代入してください。
		
		model.addAttribute("product", product);
		return ""; // 「product/result」を表示してください。
	}
	
	@GetMapping("/delete/{id}")
	             //URLからのidを取得できるアノテーションを付けてください
	public String deleteProduct(int id) {
		
		//deleteByIdメソッドを実行してください
		
		//「/product/findAll」にリダイレクトしてください。
		return ""; 
	}
	
}
