package jp.co.trainocate.answer.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.ProductRepository;

@Controller
@RequestMapping("product")
public class ProductController {
	@Autowired
	private ProductRepository prodRepo;
	
	
	
	@GetMapping("/findAll")
	public String showProductList(Model model) {
		List<Product> list = prodRepo.findAll();
		System.out.println(list);
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/")
	public String showSearchView() {
		return "product/search";
	}

	@GetMapping("/findById/{id}")
	public String showProductById(@PathVariable int id, Model model) {
		Product product = prodRepo.findById(id).orElse(null);
		model.addAttribute("product", product);
		return "product/detail";
	}

	@GetMapping("/findByPrice")
	public String showProductListByPrice(int price, Model model) {
		List<Product> list = prodRepo.findByPrice(price);
		System.out.println(list);
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/findByNameAndPrice")
	public String showProductListByNameAndPrice(String name, int price, Model model) {
		List<Product> list = prodRepo.findByNameAndPrice(name, price);
		System.out.println(list);
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/insert")
	public String showProductInsertView() {
		return "product/insert";
	}

	@PostMapping("/insert")
	public String insertProduct(ProductForm productForm) {
		Product product = new Product();
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		prodRepo.save(product);
		return "redirect:/product/findAll";
	}

	@GetMapping("update/{id}")
	public String showUpdateInputView(@PathVariable int id, Model model) {
		Product product = prodRepo.findById(id).orElse(null);
		model.addAttribute("product", product);
		return "product/update_input";
	}

	@PostMapping("/update")
	public String updateProduct(ProductForm productForm) {
		Product product = new Product();
		product.setId(productForm.getId());
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		prodRepo.save(product);
		return "redirect:/product/findAll";
	}

	//参考
	@PostMapping("/insertOrUpdate")
	public String insertOrUpdateProduct(ProductForm productForm) {
		Product product = new Product();
		if (productForm.getId() != null) {
			// IDがある場合は、既存の商品として扱い、そのIDを設定
			product.setId(productForm.getId());
		}
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		prodRepo.save(product); // 新しい商品を追加または既存の商品を更新
		return "redirect:/product/findAll";
	}
	
	@GetMapping("/delete/{id}")
	public String deleteProduct(@PathVariable int id) {
		prodRepo.deleteById(id);
		return "redirect:/product/findAll";
	}
	

}
