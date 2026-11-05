package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;

@Controller
@RequestMapping("/product2")

//このクラスには、サービスクラスを適用する用途で活用してください。

public class ProductController2 {

	
	@GetMapping("/findAll")
	public String showProductList(Model model) {
		
		
		return "product/list";
	}
	
	
	@GetMapping("/")
	public String showSearchView() {
		return "product/search";
	}
	
	@GetMapping("/findById")
	public String showProductById(int id, Model model) {
		
		
		return "product/detail";
	}
	
	@GetMapping("/findByPrice")
	public String showProductListByPrice(int price, Model model) {
		
		return "product/list";
	}
	
	@GetMapping("/findByNameAndPrice")
	public String showProductListByNameAndPrice(String name, int price, Model model) {
		
		return "product/list";
	}
	
	@GetMapping("/insert")
	public String showProductInsertView() {
		return "product/insert";
	}
	
	@PostMapping("/insert")
	public String insertProduct(ProductForm productForm, Model model) {
		Product product = new Product();
		
		
		model.addAttribute("product", product);
		return ""; // 「product/result」を表示してください。
	}
	
	@GetMapping("update/{id}")
	                    //URLからのidを取得できるアノテーションを付けてください
	public String showUpdateInputView(int id, Model model) {
		
		
		return "product/update_input";
	}

	@PostMapping("/update")
	public String updateProduct(ProductForm productForm, Model model) {
		Product product = new Product();
		
		model.addAttribute("product", product);
		return ""; // 「product/result」を表示してください。
	}
	
	@GetMapping("/delete/{id}")
	             //URLからのidを取得できるアノテーションを付けてください
	public String deleteProduct(int id) {
		
		
		//「/product/findAll」にリダイレクトしてください。
		return ""; 
	}
	
}