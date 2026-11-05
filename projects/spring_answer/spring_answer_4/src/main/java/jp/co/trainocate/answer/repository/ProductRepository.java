package jp.co.trainocate.answer.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.answer.entity.Product;

public interface ProductRepository extends JpaRepository<Product, Integer>{
	List<Product> findByPrice(Integer price); 
	List<Product> findByNameAndPrice(String name, Integer price);
	
	// その他のメソッドの例

	// SQL: SELECT * FROM product WHERE id = ? OR price = ?;
	List<Product> findByIdOrPrice(int id, int price);

	// SQL: SELECT * FROM product WHERE name <> ?;
	List<Product> findByNameNot(String name);

	// SQL: SELECT * FROM product WHERE name LIKE ?;
	List<Product> findByNameLike(String name);

	// SQL: SELECT * FROM product WHERE price IS NULL;
	List<Product> findByPriceIsNull();

	// SQL: SELECT * FROM product WHERE price IS NOT NULL;
	List<Product> findByPriceIsNotNull();

	// SQL: SELECT * FROM product WHERE name = ? ORDER BY price DESC;
	List<Product> findByNameOrderByPriceDesc(String name);

	// SQL: SELECT * FROM product WHERE price > ?;
	List<Product> findByPriceGreaterThan(int price);

	// SQL: SELECT * FROM product WHERE price < ?;
	List<Product> findByPriceLessThan(int price);

	// SQL: SELECT * FROM product WHERE price BETWEEN ? AND ?;
	List<Product> findByPriceBetween(int start, int end);

}
