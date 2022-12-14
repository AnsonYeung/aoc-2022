#include <compare>
#include <fstream>
#include <iostream>
#include <memory>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

struct Packet {
    bool is_val;
    int val;
    std::vector<std::unique_ptr<Packet>> content;

    Packet(int _val) : is_val(true), val(_val) {}
    Packet(std::vector<std::unique_ptr<Packet>> &&c)
        : is_val(false), content(std::move(c)) {}

    Packet(const Packet &other) : is_val(other.is_val), val(other.val) {
        for (auto &pack : other.content) {
            content.push_back(std::make_unique<Packet>(*pack));
        }
    }

    Packet(Packet &&other) = default;
    Packet &operator=(Packet &&other) = default;

    Packet(std::istream &is) {
        std::istream::sentry s(is);
        if (is.peek() != '[') {
            is_val = true;
            is >> val;
            return;
        }
        is_val = false;

        is.get();
        while (is.peek() != ']') {
            content.push_back(std::make_unique<Packet>(is));
            if (is.peek() == ',') is.get();
        }
        is.get();
    }

    void print() const {
        if (is_val) {
            std::cout << val;
            return;
        }
        std::cout << '[';
        int i = 0;
        for (auto &pack : content) {
            pack->print();
            if (i != content.size() - 1) std::cout << ',';
            ++i;
        }
        std::cout << ']';
    }

    std::strong_ordering operator<=>(const Packet &other) const {
        if (is_val && other.is_val) return val <=> other.val;
        const Packet *p1 = this;
        const Packet *p2 = &other;
        std::optional<Packet> t1;
        std::optional<Packet> t2;
        if (p1->is_val) {
            std::unique_ptr<Packet> temp[] = {
                std::make_unique<Packet>(p1->val)};
            t1.emplace(Packet({std::make_move_iterator(std::begin(temp)),
                               std::make_move_iterator(std::end(temp))}));
            p1 = &*t1;
        }
        if (p2->is_val) {
            std::unique_ptr<Packet> temp[] = {
                std::make_unique<Packet>(p2->val)};
            t2.emplace(Packet({std::make_move_iterator(std::begin(temp)),
                               std::make_move_iterator(std::end(temp))}));
            p2 = &*t2;
        }

        for (int i = 0; i < p1->content.size() && i < p2->content.size(); ++i) {
            std::strong_ordering res = *p1->content[i] <=> *p2->content[i];
            if (!(res == 0)) return res;
        }

        return p1->content.size() <=> p2->content.size();
    }

    bool operator==(const Packet &other) const {
        if (is_val && other.is_val) return val == other.val;
        const Packet *p1 = this;
        const Packet *p2 = &other;
        std::optional<Packet> t1;
        std::optional<Packet> t2;
        if (p1->is_val) {
            std::unique_ptr<Packet> temp[] = {
                std::make_unique<Packet>(p1->val)};
            t1.emplace(Packet({std::make_move_iterator(std::begin(temp)),
                               std::make_move_iterator(std::end(temp))}));
            p1 = &*t1;
        }
        if (p2->is_val) {
            std::unique_ptr<Packet> temp[] = {
                std::make_unique<Packet>(p2->val)};
            t2.emplace(Packet({std::make_move_iterator(std::begin(temp)),
                               std::make_move_iterator(std::end(temp))}));
            p2 = &*t2;
        }

        if (p1->content.size() != p2->content.size()) return false;

        for (int i = 0; i < p1->content.size() && i < p2->content.size(); ++i) {
            if (*p1->content[i] != *p2->content[i]) return false;
        }

        return true;
    }
};

Packet make_packet(std::string s) {
    std::stringstream ss(s);
    return Packet(ss);
}

void solve1() {
    std::fstream f("input.txt");
    int ans = 0;
    int i = 0;
    while (f.peek() != EOF) {
        Packet p1(f);
        Packet p2(f);
        if (p1 <= p2) {
            ans += i + 1;
        }
        ++i;
    }
    std::cout << ans << '\n';
}

void solve2() {
    std::fstream f("input.txt");
    std::vector<Packet> packs;
    while (f.peek() != EOF) {
        packs.emplace_back(f);
        packs.emplace_back(f);
    }
    Packet p1 = make_packet("[[2]]");
    Packet p2 = make_packet("[[6]]");
    packs.push_back(p1);
    packs.push_back(p2);
    std::sort(packs.begin(), packs.end());
    int i1 = std::find(packs.begin(), packs.end(), p1) - packs.begin() + 1;
    int i2 = std::find(packs.begin(), packs.end(), p2) - packs.begin() + 1;
    std::cout << i1 * i2 << '\n';
}

int main() {
    solve1();
    solve2();
}
