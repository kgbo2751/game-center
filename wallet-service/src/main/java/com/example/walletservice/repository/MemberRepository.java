package com.example.walletservice.repository;

import com.example.walletservice.entity.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface MemberRepository extends JpaRepository<Member, String> {
    List<Member> findTop5ByOrderByBalanceDesc();
}
