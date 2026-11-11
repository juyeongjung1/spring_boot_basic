package jp.co.trainocate.answer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jakarta.validation.Valid;
import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.CategoryRepository;
import jp.co.trainocate.answer.repository.ProductRepository;

@Controller
@RequestMapping("/product/validation")
public class ProductUpdateController {
    @Autowired
    private ProductRepository prodRepo;

    @Autowired
    private CategoryRepository cateRepo;

    @GetMapping("/update/{id}")
    public String showUpdateForm(@PathVariable int id,
            ProductForm productForm, Model model) {
        Product product = prodRepo.findById(id).orElse(null);
        if (product == null) {
            return "redirect:/product/findAll";
        }
        productForm.setId(product.getId());
        productForm.setName(product.getName());
        productForm.setPrice(product.getPrice());
        productForm.setCategoryId(product.getCategoryId());
        model.addAttribute("categories", cateRepo.findAll());
        return "product/validation_update";
    }

    @PostMapping("/update")
    public String updateProduct(@Valid ProductForm productForm,
            BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("categories", cateRepo.findAll());
            return "product/validation_update";
        }

        Integer id = productForm.getId();
        if (id == null) {
            return "redirect:/product/findAll";
        }
        Product product = prodRepo.findById(id).orElse(null);
        if (product == null) {
            return "redirect:/product/findAll";
        }
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        product.setCategoryId(productForm.getCategoryId());
        prodRepo.save(product);
        return "redirect:/product/findAll";
    }
}
