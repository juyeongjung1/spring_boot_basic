package jp.co.trainocate.answer.service;

import java.util.List;

import org.springframework.stereotype.Service;

import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.ProductRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService {

	private final ProductRepository prodRepo;

	@Override
	public Product findProductById(int id) {
		return prodRepo.findById(id).orElse(null);
	}

	@Override
	public List<Product> findAllProducts() {
		return prodRepo.findAll();
	}

	@Override
	public List<Product> findProductsByPrice(int price) {
		return prodRepo.findByPrice(price);
	}

	@Override
	public List<Product> findProductsByNameAndPrice(String name, int price) {
		return prodRepo.findByNameAndPrice(name, price);
	}

	@Override
	public Product saveProduct(ProductForm productForm) {
		Product product = new Product();
		if (productForm.getId() != null) {
			// IDがある場合は、既存の商品として扱い、そのIDを設定
			product.setId(productForm.getId());
		}
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		//登録又は更新
		product = prodRepo.save(product);
		return product;
	}

	@Override
	public void deleteProduct(int id) {
		prodRepo.deleteById(id);
	}
}
