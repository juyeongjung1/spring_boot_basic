package jp.co.trainocate.enshu.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.enshu.entity.Location;

public interface LocationRepository extends JpaRepository<Location, Integer>{
	 // 追加のメソッドは不要。基本的なCRUDメソッドがすでに使えます。
}
