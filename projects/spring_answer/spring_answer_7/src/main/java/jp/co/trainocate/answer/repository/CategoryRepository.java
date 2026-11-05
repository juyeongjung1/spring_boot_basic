package jp.co.trainocate.answer.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.answer.entity.Category;

public interface CategoryRepository extends JpaRepository<Category, Integer> {

}
