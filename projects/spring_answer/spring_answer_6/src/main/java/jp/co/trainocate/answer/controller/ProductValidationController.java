package jp.co.trainocate.answer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.server.ResponseStatusException;

import jakarta.validation.Valid;
import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.CategoryRepository;
import jp.co.trainocate.answer.repository.ProductRepository;

@Controller
@RequestMapping("/product/validation")
public class ProductValidationController {
    private final ProductRepository prodRepo;
    private final CategoryRepository cateRepo;

    public ProductValidationController(ProductRepository prodRepo,
            CategoryRepository cateRepo) {
        this.prodRepo = prodRepo;
        this.cateRepo = cateRepo;
    }

    @GetMapping("/insert")
    public String showInsertForm(ProductForm productForm,
            Model model) {
        return showForm(model, null);
    }

    @GetMapping("/update/{id}")
    public String showUpdateForm(@PathVariable int id,
            Model model) {
        Product product = findProduct(id);

        ProductForm productForm = new ProductForm();
        productForm.setName(product.getName());
        productForm.setPrice(product.getPrice());
        productForm.setCategoryId(product.getCategoryId());
        model.addAttribute("productForm", productForm);
        return showForm(model, id);
    }

    private String showForm(Model model, Integer id) {
        model.addAttribute("categories", cateRepo.findAll());
        model.addAttribute("productId", id);
        return "product/validation_form";
    }

    @PostMapping("/insert")
    public String insertProduct(@Valid ProductForm productForm,
            BindingResult result, Model model) {
        validateCategory(productForm, result);
        if (result.hasErrors()) {
            return showForm(model, null);
        }

        return saveProduct(new Product(), productForm);
    }

    @PostMapping("/update/{id}")
    public String updateProduct(@PathVariable int id,
            @Valid ProductForm productForm, BindingResult result,
            Model model) {
        Product product = findProduct(id);
        validateCategory(productForm, result);
        if (result.hasErrors()) {
            return showForm(model, id);
        }

        return saveProduct(product, productForm);
    }

    private void validateCategory(ProductForm productForm,
            BindingResult result) {
        if (!result.hasFieldErrors("categoryId")
                && !cateRepo.existsById(productForm.getCategoryId())) {
            result.rejectValue("categoryId", "product.category.invalid");
        }
    }

    private Product findProduct(int id) {
        return prodRepo.findById(id).orElseThrow(
                () -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND));
    }

    private String saveProduct(Product product,
            ProductForm productForm) {
        product.setName(productForm.getName());
        product.setPrice(productForm.getPrice());
        product.setCategoryId(productForm.getCategoryId());
        prodRepo.save(product);
        return "redirect:/product/findAll";
    }
}
