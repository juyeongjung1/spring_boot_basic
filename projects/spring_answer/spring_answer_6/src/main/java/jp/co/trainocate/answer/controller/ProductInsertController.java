package jp.co.trainocate.answer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jakarta.validation.Valid;
import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.CategoryRepository;
import jp.co.trainocate.answer.repository.ProductRepository;

@Controller
@RequestMapping("/product/validation")
public class ProductInsertController {
    @Autowired
    private ProductRepository prodRepo;

    @Autowired
    private CategoryRepository cateRepo;

    @GetMapping("/insert")
    public String showInsertForm(ProductForm productForm,
            Model model) {
        model.addAttribute("categories", cateRepo.findAll());
        return "product/validation_insert";
    }

    @PostMapping("/insert")
    public String insertProduct(@Valid ProductForm productForm,
            BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("categories", cateRepo.findAll());
            return "product/validation_insert";
        }

        Product product = new Product();
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        product.setCategoryId(productForm.getCategoryId());
        prodRepo.save(product);
        return "redirect:/product/findAll";
    }
}
