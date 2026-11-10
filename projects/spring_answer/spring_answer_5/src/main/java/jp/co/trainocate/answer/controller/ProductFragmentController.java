package jp.co.trainocate.answer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.server.ResponseStatusException;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.service.ProductService;

@Controller
@RequestMapping("/product/fragment")
public class ProductFragmentController {
    private final ProductService productService;

    public ProductFragmentController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping("/list")
    public String showProductList(Model model) {
        model.addAttribute("products",
                productService.findAllProducts());
        return "fragment_sample/list2";
    }

    @GetMapping("/detail/{id}")
    public String showProductDetail(@PathVariable int id, Model model) {
        Product product = productService.findProductById(id);
        if (product == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
        model.addAttribute("product", product);
        return "fragment_sample/detail2";
    }

    @GetMapping("/insert")
    public String showInsertForm() {
        return "fragment_sample/insert2";
    }

    @PostMapping("/insert")
    public String insertProduct(ProductForm productForm) {
        Product product = new Product();
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        productService.saveProduct(product);
        return "redirect:/product/fragment/list";
    }
}
