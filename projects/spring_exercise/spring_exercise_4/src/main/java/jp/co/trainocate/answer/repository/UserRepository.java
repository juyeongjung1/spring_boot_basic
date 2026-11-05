package jp.co.trainocate.answer.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.answer.entity.User;

public interface UserRepository extends JpaRepository<User, Integer>{
	
	//empIdとPaswordのAnd検索で、ログイン認証ができます。
	public User findByEmpIdAndPassword(Integer empId, String password);
}
