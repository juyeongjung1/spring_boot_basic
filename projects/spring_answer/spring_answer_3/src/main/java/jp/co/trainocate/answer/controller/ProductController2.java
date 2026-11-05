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
import jp.co.trainocate.answer.service.ProductServiceImpl;

@Controller
@RequestMapping("/product2")
public class ProductController2 {

	@Autowired
	private ProductServiceImpl prodService;
	
	@GetMapping("/")
	public String showSearchView() {
		return "product2/search";
	}
	
	@GetMapping("/findAll")
    public String showProductList(Model model) {
        List<Product> list = prodService.findAllProducts();
        model.addAttribute("products", list);
        return "product2/list";
    }

    @GetMapping("/findById")
    public String showProductById(int id, Model model) {
        Product product = prodService.findProductById(id);
        model.addAttribute("product", product);
        return "product2/detail";
    }
    
    @GetMapping("/findByPrice")
    public String showProductListByPrice(int price, Model model) {
        List<Product> list = prodService.findProductsByPrice(price);
        model.addAttribute("products", list);
        return "product2/list";
    }

    @GetMapping("/findByNameAndPrice")
    public String showProductListByNameAndPrice(String name, int price, Model model) {
        List<Product> list = prodService.findProductsByNameAndPrice(name, price);
        model.addAttribute("products", list);
        return "product2/list";
    }

    @GetMapping("/insert")
	public String showProductInsertView() {
		return "product2/insert";
	}
    
    @PostMapping("/insert")
    public String insertProduct(ProductForm productForm, Model model) {
        Product product = prodService.saveProduct(productForm);
        model.addAttribute("product", product);
		return "product2/result";
    }
    
    @GetMapping("update/{id}")
    public String showUpdateInputView(@PathVariable int id, Model model) {
        Product product = prodService.findProductById(id);
        model.addAttribute("product", product);
        return "product2/update_input";
    }

    @PostMapping("/update")
    public String updateProduct(ProductForm productForm, Model model) {
        Product product = prodService.saveProduct(productForm);
        model.addAttribute("product", product);
		return "product2/result";
    }

    @GetMapping("/delete/{id}")
	public String deleteProduct(@PathVariable int id) {
    	prodService.deleteProduct(id);
		return "redirect:/product2/findAll";
	}
}
