package jp.co.trainocate.answer.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.repository.ProductRepository;

@Service
public class ProductService {
	@Autowired
	private ProductRepository prodRepo;
	
	public List<Product> findAllProducts() {
        return prodRepo.findAll();
    }

    public Product findProductById(int id) {
        return prodRepo.findById(id).orElse(null);
    }

    public List<Product> findProductsByPrice(int price) {
        return prodRepo.findByPrice(price);
    }

    public List<Product> findProductsByNameAndPrice(String name, int price) {
        return prodRepo.findByNameAndPrice(name, price);
    }

    public void saveProduct(Product product) {
        prodRepo.save(product);
    }
    
    public void deleteProduct(int id) {
        prodRepo.deleteById(id);
    }
}
