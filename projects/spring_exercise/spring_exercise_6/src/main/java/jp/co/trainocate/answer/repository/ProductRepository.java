package jp.co.trainocate.answer.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.answer.entity.Product;

public interface ProductRepository extends JpaRepository<Product, Integer>{
	
	//【↓全件検索ができる@Queryアノテーションを付与してください。】
	
	//List<Product> findAllProducts();
	
	
	//【idで検索する@Queryアノテーションを付与してください。】
	
	//Product findProductById(int id);
	
	//【商品名はLIKE検索、商品名はAND検索するJPQLを@Queryアノテーションで付与してください。】
	
	//List<Product> findByNameContainingAndPrice(String name, int price);
	
	
	//5章までのメソッド
	List<Product> findByPrice(Integer price); 
	List<Product> findByNameAndPrice(String name, Integer price);
	
	
}
