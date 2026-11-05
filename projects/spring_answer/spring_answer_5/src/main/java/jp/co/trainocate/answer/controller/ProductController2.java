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
import jp.co.trainocate.answer.service.ProductService;

@Controller
@RequestMapping("product2")
public class ProductController2 {
	@Autowired
	private ProductService prodService;
	
	@GetMapping("/")
	public String showSearchView() {
		return "product/search";
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
        return "product/detail";
    }
    
    @GetMapping("/findByPrice")
    public String showProductListByPrice(int price, Model model) {
        List<Product> list = prodService.findProductsByPrice(price);
        model.addAttribute("products", list);
        return "product/list";
    }

    @GetMapping("/findByNameAndPrice")
    public String showProductListByNameAndPrice(String name, int price, Model model) {
        List<Product> list = prodService.findProductsByNameAndPrice(name, price);
        model.addAttribute("products", list);
        return "product/list";
    }

    @PostMapping("/insert")
    public String insertProduct(ProductForm productForm) {
        Product product = new Product();
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        prodService.saveProduct(product);
        return "redirect:/product/findAll";
    }
    
    @GetMapping("update/{id}")
    public String showUpdateInputView(@PathVariable int id, Model model) {
        Product product = prodService.findProductById(id);
        model.addAttribute("product", product);
        return "product/update_input";
    }

    @PostMapping("/update")
    public String updateProduct(ProductForm productForm) {
        Product product = new Product();
        product.setId(productForm.getId());
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        prodService.saveProduct(product);
        return "redirect:/product/findAll";
    }

    @PostMapping("/insertOrUpdate")
    public String insertOrUpdateProduct(ProductForm productForm) {
        Product product = new Product();
        if (productForm.getId() != null) {
            product.setId(productForm.getId());
        }
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        prodService.saveProduct(product); 
        return "redirect:/product/findAll";
    }
    
    @GetMapping("/delete/{id}")
	public String deleteProduct(@PathVariable int id) {
    	prodService.deleteProduct(id);
		return "redirect:/product/findAll";
	}
}
