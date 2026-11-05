package jp.co.trainocate.answer.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.answer.entity.User;

public interface UserRepository extends JpaRepository<User, Integer>{
	public User findByEmpIdAndPassword(Integer empId, String password);
}
