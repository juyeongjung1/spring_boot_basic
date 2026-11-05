package jp.co.trainocate.answer.service;

import java.util.List;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;

public interface ProductService {
	
	public Product findProductById(int id);
	
	public List<Product> findAllProducts();

    public List<Product> findProductsByPrice(int price);

    public List<Product> findProductsByNameAndPrice(String name, int price);

    public Product saveProduct(ProductForm productForm);
    
    public void deleteProduct(int id);
}

