package jp.co.trainocate.answer.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import jp.co.trainocate.answer.entity.Product;

public interface ProductRepository extends JpaRepository<Product, Integer> {
	
	@Query("SELECT p FROM Product p")
	List<Product> findAllProducts();

	@Query("SELECT p FROM Product p WHERE p.id = :id")
	Product findProductById(int id);

	@Query("SELECT p FROM Product p WHERE p.name LIKE %:name% AND p.price = :price")
	List<Product> findByNameContainingAndPrice(String name, int price);

	
	//【参考】複雑な仕様の例題のサンプル➀
	/*@Query("SELECT p FROM Product p LEFT JOIN p.category c " +
			"WHERE p.name LIKE %:keyword% " +
			"OR c.name LIKE %:keyword% " +
			"OR p.description LIKE %:keyword% " +
			"OR p.brand LIKE %:keyword% " +
			"OR p.sku LIKE %:keyword%")
	List<Product> searchProductsByKeyword(String keyword);*/
	
	
	//【参考】複雑な仕様の例題のサンプル➁
	/*@Query("SELECT p FROM Product p WHERE p.name LIKE %:keyword% " +
           "OR p.category.name LIKE %:keyword% " +
           "OR p.description LIKE %:keyword% " +
           "OR p.brand LIKE %:keyword% " +
           "OR p.sku LIKE %:keyword%")
	List<Product> searchProductsByKeyword(String keyword);*/

	//5章までのメソッド
	List<Product> findByPrice(Integer price);

	List<Product> findByNameAndPrice(String name, Integer price);

}
